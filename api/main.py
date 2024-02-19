import os

import dotenv
import openai
import requests
import uvicorn
import json
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from helpers import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Alive"}

@app.get("/positions")
async def get_positions():
    positions = database.select(query="SELECT * FROM positions")
    return positions

@app.get("/news")
async def get_news():
    """
    Get the latest news about bitcoin from stocktwits
    """
    response = requests.get("https://stocktwits.com/symbol/BTC.X/news")
    soup = BeautifulSoup(response.content,features="html.parser")
    news_elements = soup.find_all("div",class_='NewsItem_textContainer__6FGsX')
    content = str()
    for index,news in enumerate(news_elements):
        title = news.find("span", class_="")
        date = news.find("span",class_="text-light-grey")
        content+=f"{index+1}. {title.text} - {date.text.split('•')[1]}\n"



    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")


    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {
            "role": "system", 
            "content": (
                "You will be provided with a list of news titles about the bitcoin market."
                "Your task is to give the overall sentiment as positive, neutral, or negative."
                "Give the average time of the news."
                "Then make a general summary of 200 characters about the current market state, it will be used for a blog post."
                )
            },
            {
            "role": "assistant", 
            "content": '{"sentiment" : ..., "summary" : ...,"time": ...}'
            },
            {
            "role": "user",
            "content": content
            }
        ]
    )
    
    return json.loads(response['choices'][0]['message']['content'])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, log_level="info",reload=True)