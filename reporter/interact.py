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
    list_of_articles: list = []
    set_of_articles: set = set()
    aticle_number = 0
    logger.error(f"started at {time.strftime('%X')}")
    tasks = [Coindesk.details(article, symbol) for page in Coindesk.search(symbol=symbol, MAX_PAGE=MAX_PAGE) for article in page]
    logger.error(f"starting coroutine at {time.strftime('%X')}")
    results = await asyncio.gather(*tasks)
    logger.error(f"finished at {time.strftime('%X')}")
    return results[:MAX_ARTICLE]


if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(
        "interact:app", host="0.0.0.0", port=5050, log_level="info", reload=True
    )
