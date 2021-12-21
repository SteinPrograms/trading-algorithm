import settings, os
from database import Database
import datetime as dt
import time


class DataRetriever:
    def __init__(self):
        self.broker = settings.Settings().broker
        self.watchlist = settings.Settings().watchlist
        self.base_asset = settings.Settings().base_asset
        self.retrieve_data()

    @staticmethod
    def cls():
        """
        This function clear the terminal in order to get the clear view of the prints.c
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def retrieve_data(self):
        """
        Use the watchlist to :
        - Collect data from the broker's API. 
        - Save prices in the database every minute.
        """
        # Use timedelta to ensure every minute data (because it takes more than 1s with time.sleep + execution time)
        Database().database_request("DELETE FROM price_history", commit=True)
        try:
            start_time = time.time()

            while True:
                if dt.datetime.now().second == 0:
                    while True:
                        try:
                            self.cls()
                            print(dt.timedelta(seconds=round(time.time(), 0) - round(start_time, 0)))
                            prices = self.broker.prices(self.watchlist, self.base_asset)
                            for pair in prices:
                                Database().database_request(
                                    sql="REPLACE INTO price_history (date,price,ask,bid) VALUES (%s,%s,%s,%s)", params=(
                                        dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        (pair['ask']+pair['bid'])/2, pair['ask'], pair['bid'],
                                        ), commit=True)

                            # Print progress bar during 50 seconds
                            items = list(range(40))
                            length = len(items)
                            # Initial call to print 0% progress
                            self.print_progress_bar(0, length, prefix='Time Before Next Data Retrieve:', length=50)
                            for i, item in enumerate(items):
                                time.sleep(1)
                                # Update Progress Bar
                                self.print_progress_bar(i + 1, length, prefix='Time Before Next Data Retrieve:',
                                                        length=50)

                            break

                        except Exception as error:
                            print(error)
        except Exception as e:

            print(e)

    @staticmethod
    def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
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
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
        # Print New Line on Complete
        if iteration == total:
            print()


if __name__ == '__main__':
    DataRetriever()
