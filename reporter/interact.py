"""
API to fetch news from coindesk
"""

# Import the required libraries
import os
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException
from uvicorn.config import LOGGING_CONFIG
from fastapi.middleware.cors import CORSMiddleware
from log import logger
import asyncio
import time
import itertools
from dotenv import load_dotenv
from coindesk import Coindesk
from crypto import Crypto

load_dotenv()
# Create the fastapi app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class APIKEY(BaseModel):
    api_key: str
@app.post("/news")
async def news(
    item: APIKEY,
    symbol: str = "BTC",
    MAX_PAGE: int = 1,
    MAX_ARTICLE: int = 3,
    summarize: bool = False,
) :
    """
    With `/news` endpoint you get
    detailed articles from different sources
    for a given symbol.

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
    if item.api_key != os.getenv("STEINPROGRAMS_API_KEY"):
        logger.error(f"api_key: {item.api_key}")
        raise HTTPException(
            status_code=403, detail
            =f"API KEY {item.api_key} is not valid"
        )

    logger.info(f"started at {time.strftime('%X')}")
    # First we fetch asyncronously the articles urls from coindesk
    # Through different pages
    search_functions = [Coindesk.search, Crypto.search] #, Yahoo.search, Twitter.search, Binance.search, Kraken.searc
    task_urls = [
        search(symbol=symbol, page=page)
        for search in search_functions
        for page in range(1, MAX_PAGE + 1)
    ]
    logger.info(f"starting to search for articles at {time.strftime('%X')}")
    articles_undetailed = await asyncio.gather(*task_urls)
    logger.info(f"finished search at {time.strftime('%X')}")
    # Flatten the list of lists
    combined_list = list(itertools.chain(*articles_undetailed))

    # We should sort articles by date (which has to be in datetime format) descending
    combined_list.sort(key=lambda article: article.DATE, reverse=True)

    for article in combined_list:
        logger.info(f"article date: {article.DATE}")
    combined_list = combined_list[:MAX_ARTICLE]  # Limit the number of articles

    # Create a list of coroutines to fetch the details of the articles on their respective websites
    tasks = [article.details() for article in combined_list]
    logger.info(f"starting articles coroutine at {time.strftime('%X')}")
    results = await asyncio.gather(*tasks)
    logger.info(f"finished at {time.strftime('%X')}")

    # Then we can summarize the articles content
    if summarize:
        tasks = [article.summarize() for article in results]
        results = await asyncio.gather(*tasks)

    results = [article.to_dict() for article in results] # Convert articles to dict for json formatting
    return results
 


if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(
        "interact:app", host="0.0.0.0", port=5050, log_level="info", reload=True
    )
