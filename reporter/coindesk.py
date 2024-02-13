from datetime import datetime
from fastapi import HTTPException
from bs4 import BeautifulSoup
import aiohttp
from log import logger
from article import Article
import os



class Coindesk:
    DOMAIN = "https://www.coindesk.com"

    class ENDPOINTS:
        search = "/pf/api/v3/content/fetch/search?query={query}"
        article = "/{link}"

    class CoindeskArticle(Article):
        async def details(self) -> Article:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(self.LINK) as response:
                        # Line to check if the request was successful
                        # However, we don't want to raise an exception here
                        # response.raise_for_status()
                        logger.info(f"coindesk article code :{response.status}")
                        soup = BeautifulSoup(await response.text(), "html.parser")
                        body = soup.find_all("div", class_="eSbCkN")
                        self.CONTENT = "".join(value.text for value in body)

                except aiohttp.ClientError as error:
                    raise HTTPException(
                        status_code=404,
                        detail=f"{error} : UNABLE TO ACCESS COINDESK ARTICLE",
                    )
            return self

    @staticmethod
    async def search(*, symbol: str = "BTC", page: int = 1) -> list:
        """
        SEARCH ALL ARTICLES URL ON COINDESK
        FOR A SPECIFIC CRYPTO SYMBOL
        THROUGH MULTIPLE PAGES
        """
        # Construct main page url
        query = f"%7B%22search_query%22%3A%22{symbol}%22%2C%22sort%22%3A0%2C%22page%22%3A{page}%2C%22filter_url%22%3A%22%22%7D"
        url = Coindesk.DOMAIN + Coindesk.ENDPOINTS.search.format(query=query)
        # Fetch url
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    # response.raise_for_status()
                    logger.info(f"coindesk search code:{response.status}")
                    json = await response.json()
                    # Get the different articles details (title, description, date, creator, section, picture)
                    items = Coindesk.parse_json_to_objects(json)
                    assert type(items) == list, "Items is not a list"
                    return items
            except aiohttp.ClientError as error:
                raise HTTPException(
                    status_code=404, detail=f"{error} : UNABLE TO ACCESS COINDESK"
                )


    @staticmethod
    def parse_json_to_objects(json:dict) -> list:
        items = json.get("items")
        return [
            Coindesk.CoindeskArticle(
                title = article["title"],
                description = article["subheadlines"],  # Subheadlines is a polished description
                creator = article["creator"],
                date = datetime.strptime(article["pubdate"], "%b %d, %Y"),
                link = Coindesk.DOMAIN + Coindesk.ENDPOINTS.article.format(link=article["link"]),
                symbol = "",
                content = "",
                section = article["primary_section"],
                picture = Coindesk.DOMAIN + article["promo_image"],
            )
            for article in items
        ]




