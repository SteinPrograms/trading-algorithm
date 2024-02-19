import requests
from bs4 import BeautifulSoup
import logging
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url:str = os.environ.get("SUPABASE_URL")
key:str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
def insert_database(article):
    data, count = supabase.table('coindesk')\
      .insert(article)\
      .execute()    
    print(data)
    print(count)
    
logger = logging.getLogger(__name__)
# Always use basic config for logging because it is the best
logging.basicConfig(level=logging.DEBUG)
MAX_PAGE= 10
def coindesk_news(symbol:str = "BTC") -> str:
    articles = list()
    for page in range(0,MAX_PAGE):
        # Construct the url
        url = f"https://www.coindesk.com/pf/api/v3/content/fetch/search?query=%7B%22search_query%22%3A%22{symbol}%22%2C%22sort%22%3A0%2C%22page%22%3A{page}%2C%22filter_url%22%3A%22%22%7D"
        # Fetch url
        response = requests.get(url)
        # Get the different articles
        items = response.json().get("items")
        for item in items:
            for key,value in item.items():
                print(key,value)
            # Get the values
            title = item["title"]
            # Subheadlines is a finished description
            # Because we get the description from the article itself
            description = item["subheadlines"]
            date = item["pubdate"]
            creator = item["creator"]
            section = item["primary_section"]
            picture = f"https://www.coindesk.com{item["promo_image"]}"
            # Fetch content of the article
            url = f"https://www.coindesk.com{item['link']}"
            print(url)
            # Now get div content at-grid-center
            response = requests.get(url)
            soup = BeautifulSoup(response.content,features="html.parser")
            # Class of content is eSbCkN
            body = soup.find_all("div",class_="eSbCkN")
            content = str()
            for values in body:
                print(values.text)
                content+=values.text
            input("Press enter to generate summary of article")
            # Create a summary of the article using mistral
            response = requests.post(
                "http://localhost:8000/mistral_summarizer/invoke",
                json={'input': {'text': content}}
            )
            print(response.json())
            summary = response.json().get("output")
            insert_database({
                "title": title,
                "description": description,
                "creator": creator,
                "date": date,
                "content": content,
                "section": section,
                "picture": picture,
                "summary": summary,
            })
            articles.append({
                "title": title,
                "summary": summary
            })
            if input("Continue? Y/N (y)").lower() == "n":
                break
        if input(f"There is {MAX_PAGE-page} left.\nContinue? Y/N (y)").lower() == "n":
            break
        print("Next page")
    print("Stopping")

    
    # Using all the summaries, create a recap (overview) of the current state around crypto
    # Create a summary of the article using mistral
    response = requests.post(
        "http://localhost:8000/mistral_redactor/invoke",
        json={'input': {'list': str(articles)}}
    )
    print(response.json())
    print(response.json().get("output"))
    return str()

coindesk_news()



