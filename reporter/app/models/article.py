
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
                    self.CONTENT = result.get("choices")[0].get("message").get("content")

            return self
    
    async def categorize(self) -> 'Article': # forward reference
        async with aiohttp.ClientSession() as session:
            # Use a pipeline as a high-level helper
            # Split the summary per keypoint and check the overall sentiment
            if self.CONTENT != "":
                headers = {
                    "Accept" : "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + os.getenv("HUGGINGFACE_API_KEY", ""),
                }
                json_data = {
                    "inputs": self.CONTENT,
                }
                for _ in range(3):
                    async with session.post(
                        os.getenv("HUGGINGFACE_ENDPOINT"), # Model can be loading {'error': 'Model ProsusAI/finbert is currently loading', 'estimated_time': 20.0}
                        headers=headers,
                        json=json_data,
                    ) as response:
                        result = await response.json()
                        logger(__name__).info(result)
                        # Check for errors
                        if 'error' in result:
                            try:
                                estimated_time = int(result["estimated_time"])
                                await asyncio.sleep(estimated_time) # suspense for X seconds
                                continue # Try again
                            except KeyError:
                                error = result.get("error") # If there is not error, it will raise an exception
                                raise HTTPException(
                                    status_code=404,
                                    detail=f"{error} : UNABLE TO ACCESS HUGGINGFACE API",
                                )
                        try:
                            self.SENTIMENT = result[0].get("label") # Can be slightly bullish if NEUTRAL first and BULLISH second
                        except:
                            self.SENTIMENT = "Unavailable"
                        break
            return self