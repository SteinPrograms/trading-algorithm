import datetime
import requests
class Log:
    def __init__(self,message):
        print(f"{datetime.datetime.now():%m/%d/%Y %H:%M:%S}    {message}")
        with open("logs.txt","a") as file:
            print(f"{datetime.datetime.now():%m/%d/%Y %H:%M:%S}    {message}",file=file)
        requests.post(url="https://api.telegram.org/bot6568731876:AAHVWrfKiAOqSuDlPa9isOKLNUtj19gRy4w/sendMessage",params={
            "chat_id":"-431364858",
            "text":message
        })

    def clean_logs(self):
        with open("logs.txt","w") as file:
            print("",file=file)
