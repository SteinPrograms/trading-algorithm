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
async def get_news(symbol: str = "BTC", MAX_PAGE: int = 1, MAX_ARTICLE: int = 1) -> list[dict]:
    list_of_articles: list = []
    set_of_articles: set = set()
    aticle_number = 0
    for page_number,page in enumerate(Coindesk.search(symbol=symbol, MAX_PAGE=MAX_PAGE)):
        logger.info(f"Fetching page {page_number+1}/{MAX_PAGE}")
        for article in page:
            details = Coindesk.details(article, symbol)
            # if the same author wrote with same symbol, same date, same title
            specificities = (details.CREATOR, details.SYMBOL, details.DATE)
            if specificities in set_of_articles:
                continue
            set_of_articles.add(specificities)
            list_of_articles.append(details.to_dict())
            aticle_number+=1
            if aticle_number == MAX_ARTICLE:
                return list_of_articles
    return list_of_articles

if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(
        "interact:app", host="0.0.0.0", port=5050, log_level="info", reload=True
    )
