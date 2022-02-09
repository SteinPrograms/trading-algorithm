from database import Database
from brokerconnection import RealCommands
import datetime as dt
import time

while(True):
    now = dt.datetime.now()
    #Every day at 8AM
    if now.hour == 8 and now.minute == 0 and now.second == 0:
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
                    RealCommands().balance_check(),
                ),
                commit=True,
            )
            time.sleep(60)
        except Exception as e :
            print(e)