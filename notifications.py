import requests

from database import Database




class Telegram:
    def __init__(self):
        pass
    
    
    def program_notification(self,message):
        try:
            telegram_data = Database().database_request(sql="""SELECT * FROM telegram""", fetchone=True)
            token = telegram_data["token"]
            chat_id = telegram_data["chat_id"]

            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
            requests.post(url)
        except Exception as error:
            print(error)