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

@app.get("/news/")
async def get_news(password:str, symbol:str = "BTC"):
    """
    Get the latest news about bitcoin from stocktwits
    """
    if password != os.getenv("STEIN_API_KEY"):
        return {"message":"Unauthorized"}
    response = requests.get(f"https://stocktwits.com/symbol/{symbol}.X/news")
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
                "Your are a crypto market analyst. Don't take into consideration everything you already know about the crypto market."
                f"You will be provided with a list of news titles about the {symbol} crypto market."
                "Your task is to give the overall sentiment as positive, slightly-positive, neutral, slightly-negative or negative."
                "Then make a general summary of around 250 characters about the news, it will be used for a blog post."
                "Your answer is a json object, the time key represents the average news time."
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
    
    print(content)

    return json.loads(response['choices'][0]['message']['content'])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, log_level="info",reload=True)