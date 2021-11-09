"""

Ce programme sert à inserer les prix des différentes crypto toutes les minutes dans la base de données.

Cela permet de créer nos propres analyses et graphiques seulement à partir des prix.


"""


import settings,os
from database import Database
import datetime as dt
import time




class data_retriever:
    def __init__(self):
        self.broker = settings.Settings().broker
        self.watchlist = settings.Settings().watchlist
        self.base_asset = settings.Settings().base_asset
        Database().database_request(sql="""DELETE FROM prices""",commit=True)
        self.retrieve_data()
        
        
    def cls(self):
        """
        This function clear the terminal in order to get the clear view of the prints.c
        """
        os.system('cls' if os.name=='nt' else 'clear')
        
    

    def retrieve_data(self):
        """
        Use the watchlist to :
        - Collect data from the broker's API. 
        - Save prices in the database every minute.
        """
        #Use timedelta to ensure every minute data (because it takes more than 1s with time.sleep + execution time)
        try:
            start_time = time.time()
            
            while True:
                if dt.datetime.now().second ==0:
                    while True:
                        try:
                            self.cls()
                            print(str(dt.timedelta(seconds=round(time.time(),0)-round(start_time,0))))
                            prices = self.broker.prices(self.watchlist,self.base_asset)
                            Database().database_request("""DELETE FROM cryptocurrencies""")
                            for pair in prices:
                                Database().database_request(sql="REPLACE INTO cryptocurrencies (symbol,broker) VALUES (%s,%s)",params=(pair['symbol'],settings.Settings().broker_name),commit=True)
                                Database().database_request(sql="REPLACE INTO prices (symbol,ask,bid,date) VALUES (%s,%s,%s,%s)",params=(pair['symbol'],pair['ask'],pair['bid'],dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")),commit=True)

                            

                            # Print progress bar during 50 seconds
                            items = list(range(40))
                            l = len(items)
                            # Initial call to print 0% progress
                            self.printProgressBar(0, l, prefix = 'Time Before Next Data Retrieve:', length = 50)
                            for i, item in enumerate(items):
                                time.sleep(1)
                                # Update Progress Bar
                                self.printProgressBar(i + 1, l, prefix = 'Time Before Next Data Retrieve:', length = 50)

                            break


                        except Exception as error:
                            print(error)
        except Exception as e:
            
            print(e)

    def printProgressBar (self,iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

if __name__ == '__main__':
    data_retriever()