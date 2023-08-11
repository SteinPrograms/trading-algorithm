import datetime
class Log:
    def __init__(self,message):
        print(f"{datetime.datetime.now():%m/%d/%Y %H:%M:%S}    {message}")
        with open("logs.txt","a") as file:
            print(f"{datetime.datetime.now():%m/%d/%Y %H:%M:%S}    {message}",file=file)
