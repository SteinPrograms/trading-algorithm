from datetime import datetime
import openai
from dotenv import load_dotenv
import json
import os
from bs4 import BeautifulSoup
import requests
from supabase import create_client, Client


def get_stocktwits_news(symbol:str = "BTC") -> str:
    print("Fetching news")
    """Get 10 latest news from stocktwits website about a crypto symbol"""
    response = requests.get(f"https://stocktwits.com/symbol/{symbol}.X/news")
    soup = BeautifulSoup(response.content,features="html.parser")
    news_elements = soup.find_all("div",class_='NewsItem_textContainer__6FGsX')
    content = str()
    for index,news in enumerate(news_elements):
        title = news.find("span", class_="")
        date = news.find("span",class_="text-light-grey")
        content+=f"{index+1}. {title.text} - {date.text.split('•')[1]}\n"
    print("News fetched")
    return content

def prepare_prompt(symbol:str = "BTC") -> str:
    return (
        "Your are a crypto market analyst writing a blog post based on news."
        "Don't take into consideration what you know."
        f"You will be provided with a list of news about the {symbol} crypto market."
        "Your role is to write a blog post about the news."
        "Your answer is a JSON object with the following keys: sentiment, summary, time."
        "summary key : Make a general readable summary of around 500 characters about the news, make transition between news. It should be easy to read"
        "title key : Find a short title for the blog post."
        "score key : Provide overall sentiment score on a scale from 0 to 100 as 0 being very negative and 100 being very positive."
    )

def publish_to_supabase(*,label:str,content:str,title:str,score:int):
    data, count = rls.table('marketnews').insert({"label": label, "content": content,"title":title,"score":score}).execute()

def ask_chat_gpt(news:str, symbol:str = "BTC") -> str:
    print('Asking GPT model')
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": prepare_prompt(symbol)
            },
            {
                "role": "assistant", 
                "content": '{"summary" : ..., "title" : ...,"score": ...}'
            },
            {
                "role": "user",
                "content": news
            }
        ]
    )


if __name__ == "__main__":
    load_dotenv()
    MINUTE = 30
    trigger = True
    while True:
        if datetime.now().minute == MINUTE and trigger:
            trigger = False
            ### OPENAI API
            openai.api_key = os.getenv("OPENAI_API_KEY")
            ### SUPABASE CLIENT
            supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
            data = supabase.auth.sign_in_with_password({"email": os.environ.get("SUPABASE_EMAIL"), "password": os.environ.get("SUPABASE_PASSWORD")})
            rls = supabase.postgrest.auth(supabase.auth.get_session().access_token)
            ### SYMBOLS TRACKED
            SYMBOL_LIST = ["BTC","ETH","XRP"]

            for symbol in SYMBOL_LIST:
                news = get_stocktwits_news(symbol)
                response = ask_chat_gpt(news=news,symbol=symbol)
                try:
                    json_response = json.loads(response['choices'][0]['message']['content'])
                    print(json_response)
                    publish_to_supabase(label=symbol,title=json_response.get('title'),content=json_response.get('summary'),score=json_response.get('score'))
                except Exception as e:
                    print(response['choices'][0]['message']['content'])
                    get_module_logger().error("error",e)
                    # GPT response invalid
                    exit()
            supabase.auth.sign_out()

        else:
            trigger = True