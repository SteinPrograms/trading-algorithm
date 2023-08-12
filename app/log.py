import datetime
import requests
import os
class Log:
    def __init__(self,message):
        print(f"{datetime.datetime.now():%m/%d/%Y %H:%M:%S}    {message}")
        with open("logs.txt","a") as file:
            print(f"{datetime.datetime.now():%m/%d/%Y %H:%M:%S}    {message}",file=file)
        requests.post(url=f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",params={
            "chat_id":os.getenv('TELEGRAM_CHAT_ID'),
            "text":message
        })

    def clean_logs(self):
        with open("logs.txt","w") as file:
            print("",file=file)
