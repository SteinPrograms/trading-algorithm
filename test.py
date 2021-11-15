from pprint import pprint

import requests

from prediction import Prediction
from database import Database
def program_notification(message):
    try:
        telegram_data = Database().database_request(sql="""SELECT * FROM telegram""", fetchone=True)
        token = telegram_data["token"]
        chat_id = telegram_data["chat_id"]
        print(token)
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.post(url)
    except Exception as error:
        print(error)


program_notification("Test")