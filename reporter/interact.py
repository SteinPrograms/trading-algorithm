"""
API to fetch news from coindesk
"""
# Import the required libraries
import os
import logging
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client, Client
from uvicorn.config import LOGGING_CONFIG
from fastapi.middleware.cors import CORSMiddleware

# Create the logger
logger = logging.getLogger(__name__)
# Always use basic config for logging because it is the best
logging.basicConfig(level=logging.DEBUG)

# Load the environment variables
load_dotenv()
try:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    assert type(url) == str, "UNABLE TO LOAD SUPABASE_URL"
    assert type(key) == str, "UNABLE TO LOAD SUPABASE_KEY"
except Exception as e:
    logger.error("Error while loading environment variables")
    logger.error(e)
    raise e

# Create the supabase client
supabase: Client = create_client(url, key)

# Create the fastapi app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def summarizer(content:str) -> str:
    # Create a summary of the article using mistral
    try:
        response = requests.post(
            "http://localhost:8000/summarizer/invoke",
            json={'input': {'text': content}}
        )
    except Exception:
        logger.error("UNABLE TO CONNECT TO SUMMARIZER API")
        raise HTTPException(status_code=404, detail="UNABLE TO CONNECT TO SUMMARIZER API")
    json_response = response.json()
    summary = json_response.get("output")
    return summary

def insert_database(article):
    data, count = supabase.table('coindesk')\
      .insert(article)\
      .execute()    
    print(count)
    return (data)
    
class Coindesk:
    def __init__(self):
        self.DOMAIN = "https://www.coindesk.com"
        self.ENDPOINTS = {
            "search": "/pf/api/v3/content/fetch/search?query={query}",
            "article": "/{link}",
        }

    def search(self, symbol:str = "BTC", MAX_PAGE:int = 10):
        # Length of search
        for page in range(0,MAX_PAGE):
            # Construct main page url
            query = f"%7B%22search_query%22%3A%22{symbol}%22%2C%22sort%22%3A0%2C%22page%22%3A{page}%2C%22filter_url%22%3A%22%22%7D" 
            url = self.DOMAIN + self.ENDPOINTS["search"].format(query=query)
            # Fetch url
            try:
                response = requests.get(url)
            except:
                raise HTTPException(status_code=404, detail="UNABLE TO ACCESS COINDESK")
            # Get the different articles details (title, description, date, creator, section, picture)
            items = response.json().get("items")
            # Test if items is a list
            assert type(items) == list, "Items is not a list"
            yield items

    def details(self, article:dict, symbol) -> dict:
        # Get the values
        title = article["title"]
        description = article["subheadlines"] # Subheadlines is a polished description
        date = article["pubdate"]
        creator = article["creator"]
        section = article["primary_section"]
        picture = self.DOMAIN + article["promo_image"]

        # Fetch content of the article
        url = self.DOMAIN + self.ENDPOINTS["article"].format(link=article["link"])
        try:
            response = requests.get(url)
        except:
            raise HTTPException(status_code=404, detail="UNABLE TO ACCESS COINDESK")
        # Init the HTML parser
        soup = BeautifulSoup(response.content,features="html.parser")
        # Class of content is eSbCkN
        body = soup.find_all("div",class_="eSbCkN")
        content = str()
        for values in body:
            content+=values.text

        # Create a short summary of the article using mistral
        summary = summarizer(content)
        return {
            "title": title,
            "description": description,
            "creator": creator,
            "date": date,
            "link": url,
            "symbol": symbol,
            "content": content,
            "section": section,
            "picture": picture,
            "summary": summary,
        }

coindesk = Coindesk()

@app.get("/news")
async def get_news(symbol:str = "BTC"):
    # if the same aurthor wrote with same symbol, same date, same title
     for page in coindesk.search(symbol=symbol):
        logger.info(f"Fetching page {page}")
        for article in page:
            details = coindesk.details(article, symbol)
            return insert_database(details)

if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run("interact:app", host="0.0.0.0", port=5050, log_level="info",reload=True)

