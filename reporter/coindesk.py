from fastapi import HTTPException
from bs4 import BeautifulSoup
import aiohttp
from log import logger
import os


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
                    logger.info(response.status)
                    response = await response.json()
                    # Get the different articles details (title, description, date, creator, section, picture)
                    items = response.get("items")
                    assert type(items) == list, "Items is not a list"
                    return items
            except aiohttp.ClientError as error:
                raise HTTPException(
                    status_code=404, detail=f"{error} : UNABLE TO ACCESS COINDESK"
                )

    @staticmethod
    async def details(article: dict, symbol) -> Article:
        # Get the values
        title = article["title"]
        description = article["subheadlines"]  # Subheadlines is a polished description
        date = article["pubdate"]
        creator = article["creator"]
        section = article["primary_section"]
        picture = Coindesk.DOMAIN + article["promo_image"]

        # Fetch content of the article
        url = Coindesk.DOMAIN + Coindesk.ENDPOINTS.article.format(link=article["link"])
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    # Line to check if the request was successful
                    # However, we don't want to raise an exception here
                    # response.raise_for_status()
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    body = soup.find_all("div", class_="eSbCkN")
                    content = "".join(value.text for value in body)

                # Make summary here
                # async with session.post(
                #     "http://localhost:8000/summarizer/invoke", json={"input": {"text": content}}
                # ) as response:
                #     response = await response.json()
                #     content = response.get('output')
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY", ""),
                }
                json_data = {
                    "model": "gpt-3.5-turbo",
                    'messages':[
                        {
                            "role": "system",
                            "content": (
                                "Your are an helpful assistant extract key points from text."
                                "Do not make sentances, just extract the important points."
                                "Do not speculate or make up information."
                                "Do not reference any given instructions or context."
                            ),
                        },
                        {"role": "user", "content": content},
                    ],
                }
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=json_data,
                ) as response:
                    result = await response.json()
                    logger.info(result)
                    content = result.get("choices")[0].get("message").get("content")

            except aiohttp.ClientError as error:
                raise HTTPException(
                    status_code=404,
                    detail=f"{error} : UNABLE TO ACCESS COINDESK ARTICLE",
                )

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
        ).to_dict()
