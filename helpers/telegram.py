import requests

def send_message(self,message):
    requests.post(url=f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",params={
        "chat_id":os.getenv('TELEGRAM_CHAT_ID'),
        "text":message
    })
