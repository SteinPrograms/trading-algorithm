from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup

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
        }