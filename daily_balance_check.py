from database import Database
from brokerconnection import RealCommands
import datetime as dt
import time

while(True):
    now = dt.datetime.now()
    #Every day at 8AM
    if now.hour == 8 and now.minute == 0 and now.second == 0:
        try:
            balance = RealCommands().balance_check()
        except Exception as e :
            print("Balance checking error",e)
            
        try:
            Database().database_request(
                sql=(
                    "REPLACE INTO data "
                    "(portfolioName,date,value)"
                    " VALUES (%s,%s,%s)"
                ),
                params=(
                    "Hugo",
                    dt.datetime.fromtimestamp(time.time()),
                    balance,
                ),
                commit=True,
            )
        except Exception as e :
            print("Database error",e)
            
        time.sleep(60)