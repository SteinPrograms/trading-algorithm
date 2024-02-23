from datetime import datetime
from fastapi import HTTPException
from bs4 import BeautifulSoup
import aiohttp
from helpers import logger
from models.article import Article

class Crypto:
    DOMAIN = 'https://crypto.news'

    class ENDPOINTS:
        search = "/{query}"

    class CryptoArticle(Article):
        async def details(self) -> Article:
            # Fetch content of the article
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(self.LINK) as response:
                        # Line to check if the request was successful
                        # However, we don't want to raise an exception here
                        # response.raise_for_status()
                        logger(__name__).info(f"crypto.news article code:{response.status}")
                        soup = BeautifulSoup(await response.text(), "html.parser")
                        content = soup.find_all(class_="post-detail__content blocks")[0]
                        self.CONTENT = ''.join([value.text for value in content if value.name in ['h2','p','ul','blockquote','a']])

                except aiohttp.ClientError as error:
                    raise HTTPException(
                        status_code=404,
                        detail=f"{error} : UNABLE TO ACCESS CRYPTO NEWS ARTICLE",
                    )
            return self

    @staticmethod
    async def search(*, symbol: str = "BTC", page: int = 1) -> list:
        """
        SEARCH ALL ARTICLES URL ON CRYPTO.NEWS
        FOR A SPECIFIC CRYPTO SYMBOL
        THROUGH MULTIPLE PAGES
        """
        # Construct search page url
        if (page == 1):
            query = f"?s={symbol}"
        else:
            query = f"page/{page}/?s={symbol}"

        url = Crypto.DOMAIN + Crypto.ENDPOINTS.search.format(query=query)
        # Fetch url
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    # response.raise_for_status()
                    logger(__name__).info(f"crypto.news search code :{response.status}")
                    response = await response.text()
                    # Get the different articles details (title, description, date, creator, section, picture)
                    items = Crypto.parse_html_to_objects(html=response, symbol=symbol)
                    assert type(items) == list, "Items is not a list"
                    return items
            except aiohttp.ClientError as error:
                raise HTTPException(
                    status_code=404, detail=f"{error} : UNABLE TO ACCESS COINDESK"
                )
    
    @staticmethod
    def parse_html_to_objects(*,html: str, symbol: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        return [
            Crypto.CryptoArticle(
                provider="Crypto News",
                title=article.find(class_='search-result-loop__title').text.strip(),
                description=article.find(class_='search-result-loop__summary').text.strip(),
                creator='Crypto News',
                date=datetime.strptime(article.find(class_='search-result-loop__date').text.strip(), "%B %d, %Y at %I:%M %p"),
                link=article.find(class_='search-result-loop__link').get('href'),
                symbol=symbol,
                content='',
                section='news',
                picture=article.find(class_='search-result-loop__image').get('src')
            )
            for article in soup.find_all(class_='search-result-loop')
        ]

