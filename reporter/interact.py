"""
API to fetch news from coindesk
"""

# Import the required libraries
import uvicorn
from fastapi import FastAPI
from uvicorn.config import LOGGING_CONFIG
from fastapi.middleware.cors import CORSMiddleware
from coindesk import Coindesk
from log import logger
import asyncio
import time
import itertools

# Create the fastapi app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/news")
async def get_news(
    symbol: str = "BTC", MAX_PAGE: int = 1, MAX_ARTICLE: int = 3
) -> list[dict]:
    logger.info(f"started at {time.strftime('%X')}")
    # First we fetch asyncronously the articles urls from coindesk
    # Through different pages
    task_urls = [Coindesk.search(symbol=symbol,page=page) for page in range(0, MAX_PAGE)]
    logger.info(f"starting pages coroutine at {time.strftime('%X')}")
    articles_urls = await asyncio.gather(*task_urls)
    logger.info(f"finished at {time.strftime('%X')}")
    combined_list = list(itertools.chain(*articles_urls))[:MAX_ARTICLE]
    # We have a list of list of url_articles
    # Create a list of coroutines
    tasks = [Coindesk.details(article, symbol) for article in combined_list]
    logger.info(f"starting articles coroutine at {time.strftime('%X')}")
    results = await asyncio.gather(*tasks)
    logger.info(f"finished at {time.strftime('%X')}")
    return results


if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(
        "interact:app", host="0.0.0.0", port=5050, log_level="info", reload=True
    )
