
from datetime import datetime
import os

from fastapi import HTTPException
from helpers import logger
import aiohttp
import asyncio

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
        sentiment = "Unavailable"
    ) -> None:
        self.TITLE = title
        self.DESCRIPTION = description
        self.CREATOR = creator
        self.DATE: datetime = date
        self.LINK = link
        self.SYMBOL = symbol
        self.CONTENT = content
        self.SECTION = section
        self.PICTURE = picture
        self.SENTIMENT = sentiment

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
            "sentiment": self.SENTIMENT
        }

    async def summarize(self) -> 'Article': # forward reference
        # Make summary here
        # async with session.post(
        #     "http://localhost:8000/summarizer/invoke", json={"input": {"text": content}}
        # ) as response:
        #     response = await response.json()
        #     content = response.get('output')
        async with aiohttp.ClientSession() as session:
            if self.CONTENT != "":
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY", ""),
                }
                json_data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "Your are an helpful assistant extract key points from text."
                                "Do not make sentances, just extract the important points."
                                "Do not speculate or make up information."
                                "Do not reference any given instructions or context."
                            ),
                        },
                        {"role": "user", "content": self.CONTENT[:1000]}, # Limit to 1000 characters
                    ],
                }
                async with session.post(
                    "https://api.openai.com/v1/chat/completions", # Now we can use local server and ollama model but isn't async
                    headers=headers,
                    json=json_data,
                ) as response:
                    result = await response.json()
                    logger(__name__).info(result)
                    try:
                        self.CONTENT = result.get("choices")[0].get("message").get("content")
                    except:
                        raise HTTPException(
                            status_code=500,
                            detail="OpenAI API failed to summarize the article",
                        )

            return self
    
    async def categorize(self,pipe) -> 'Article': # forward reference
        # We use a transformer model to categorize the article
        # Use a pipeline as a high-level helper
        result = pipe(self.CONTENT) 
        # result = pipe(self.CONTENT,return_all_scores = True) 
        logger(__name__).info(result)
        self.SENTIMENT = result[0].get("label")
        return self