import itertools
import os
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
import time
from models import Coindesk, Crypto
from helpers import logger, Database
import asyncio
from transformers import pipeline

router = APIRouter()

api_keys = Database().get_api_keys()

api_keys.append({"tier": 4, "api_key": os.environ["STEINPROGRAMS_API_KEY"]})
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

# Pipeline for sentiment analysis
pipe = pipeline("text-classification", model="ProsusAI/finbert")

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    # We load all api keys from the db and check (warning it is not efficient)
    if api_key_header in [api_key["api_key"] for api_key in api_keys]:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )


@router.get("/refresh")
def refresh(
    api_key: str = Depends(api_key_header)
):
    """
    REQUEST FROM WEB SERVER ONLY
    With `/refresh` endpoint you can
    refresh the api keys from the database.
    """
    global api_keys
    
    if api_key not in [api_key["api_key"] for api_key in api_keys if api_key["tier"] > 0]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Upgrade API key to access this feature",
            )
    api_keys = Database().get_api_keys()
    api_keys.append({"tier": 4, "api_key": os.environ["STEINPROGRAMS_API_KEY"]})
    return {"detail": "API keys refreshed"}


@router.get("/news", dependencies=[Depends(get_api_key)])
async def news(
    symbol: str = "BTC",
    MAX_PAGE: int = 1,
    MAX_ARTICLE: int = 3,
    summarize: bool = False,
    sentiment: bool = False,
    api_key: str = Depends(api_key_header)
):
    """
    With `/news` endpoint you get
    detailed articles from different sources
    for a given symbol.

    To access the endpoint you need to provide an api key
    in the header of the request with the key `X-API-KEY`.

    To access the summarize and sentiment features
    you need to have a tier 1 or above api key which
    you can get by subscribing to the service through
    [steinprograms.com](https://steinprograms.com).

    How to use with python:
    ```python
    response = requests.get("endpoint/news?symbol=BTC&MAX_PAGE=1&MAX_ARTICLE=3")
    response = response.json()

    for article in response:
        article["title"]
        article["description"]
        article["creator"]
        article["date"]
        article["link"]
        article["symbol"]
        article["content"]
        article["section"]
        article["picture"]
    ```

    How to use with javascript:
    ```javascript
    fetch('http://localhost:5050/news')
    .then(response => response.json())
    .then(data => {
        data?.map(article => {
            console.log(article.title);
            console.log(article.description);
            console.log(article.creator);
            console.log(article.date);
            console.log(article.link);
            console.log(article.symbol);
            console.log(article.content);
            console.log(article.section);
            console.log(article.picture);
        })
    });
    ```
    """

    # ACCESS TO SUMMARIZE AND SENTIMENT IS LIMITED TO TIER 1 and above
    if summarize or sentiment:
        if api_key not in [api_key["api_key"] for api_key in api_keys if api_key["tier"] > 0]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Upgrade API key to access this feature",
            )
    logger(__name__).info(f"STARTED ")
    # First we fetch asyncronously the articles urls from coindesk
    # Through different pages
    search_functions = [
        Coindesk.search,
        # Crypto.search,
    ]  # , Yahoo.search, Twitter.search, Binance.search, Kraken.searc
    task_urls = [
        search(symbol=symbol, page=page)
        for search in search_functions
        for page in range(1, MAX_PAGE + 1)
    ]
    logger(__name__).info("SEARCH ROUTINES STARTED")
    articles_undetailed = await asyncio.gather(*task_urls)
    logger(__name__).info("SEARCH ROUTINES FINISHED")
    # Flatten the list of lists
    combined_list = list(itertools.chain(*articles_undetailed))

    # We should sort articles by date (which has to be in datetime format) descending
    combined_list.sort(key=lambda article: article.DATE, reverse=True)
    combined_list = combined_list[:MAX_ARTICLE]  # Limit the number of articles

    # Create a list of coroutines to fetch the details of the articles on their respective websites
    tasks = [article.details() for article in combined_list]
    logger(__name__).info(f"ARTICLE DETAILS FETCHING STARTED")
    results = await asyncio.gather(*tasks)
    logger(__name__).info(f"ARTICLE DETAILS FETCHING FINISHED")

    # Then we can summarize the articles content
    if summarize:
        tasks = [article.summarize() for article in results]
        results = await asyncio.gather(*tasks)

    if sentiment and summarize:
        tasks = [article.categorize(pipe) for article in results]
        results = await asyncio.gather(*tasks)

    results = [
        article.to_dict() for article in results
    ]  # Convert articles to dict for json formatting
    return results
