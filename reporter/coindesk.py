from fastapi import HTTPException
from bs4 import BeautifulSoup
import requests


class Article:
    def __init__(
        self,
        *,
        title,
        description,
        creator,
        date,
        link,
        symbol,
        content,
        section,
        picture,
    ) -> None:
        self.TITLE = title
        self.DESCRIPTION = description
        self.CREATOR = creator
        self.DATE = date
        self.LINK = link
        self.SYMBOL = symbol
        self.CONTENT = content
        self.SECTION = section
        self.PICTURE = picture

    def to_dict(self):
        return {
            "title": self.TITLE,
            "description": self.DESCRIPTION,
            "creator": self.CREATOR,
            "date": self.DATE,
            "link": self.LINK,
            "symbol": self.SYMBOL,
            "content": self.CONTENT,
            "section": self.SECTION,
            "picture": self.PICTURE,
        }


class Coindesk:
    DOMAIN = "https://www.coindesk.com"
    class ENDPOINTS:
        search = "/pf/api/v3/content/fetch/search?query={query}"
        article = "/{link}"

    @staticmethod   
    def search(symbol: str = "BTC", MAX_PAGE: int = 10):
        # Length of search
        for page in range(0, MAX_PAGE):
            # Construct main page url
            query = f"%7B%22search_query%22%3A%22{symbol}%22%2C%22sort%22%3A0%2C%22page%22%3A{page}%2C%22filter_url%22%3A%22%22%7D"
            url = Coindesk.DOMAIN + Coindesk.ENDPOINTS.search.format(query=query)
            # Fetch url
            try:
                response = requests.get(url)
            except Exception as error:
                raise HTTPException(
                    status_code=404, detail=f"{error} UNABLE TO ACCESS COINDESK"
                )
            # Get the different articles details (title, description, date, creator, section, picture)
            items = response.json().get("items")
            # Test if items is a list
            assert type(items) == list, "Items is not a list"
            yield items

    @staticmethod
    def details(article: dict, symbol) -> Article:
        # Get the values
        title = article["title"]
        description = article["subheadlines"]  # Subheadlines is a polished description
        date = article["pubdate"]
        creator = article["creator"]
        section = article["primary_section"]
        picture = Coindesk.DOMAIN + article["promo_image"]

        # Fetch content of the article
        url = Coindesk.DOMAIN + Coindesk.ENDPOINTS.article.format(link=article["link"])
        try:
            response = requests.get(url)
        except:
            raise HTTPException(status_code=404, detail="UNABLE TO ACCESS COINDESK")
        # Init the HTML parser
        soup = BeautifulSoup(response.content, features="html.parser")
        # Class of content is eSbCkN
        body = soup.find_all("div", class_="eSbCkN")
        content = str()
        for values in body:
            content += values.text

        return Article(
            title=title,
            description=description,
            creator=creator,
            date=date,
            link=url,
            symbol=symbol,
            content=content,
            section=section,
            picture=picture,
        )