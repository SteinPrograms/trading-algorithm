import dotenv

# Creating trader class
class Trader:
    # Constructor for trader class without any parameters
    def __init__(self):
        # Loading environment variables
        dotenv.load_dotenv()

    # Self calibration
    def assets_trends(self):
        pass

    # Fetches news 
    def fetch_news(self):
        """
        Method that go through list
        of news sources and fetches
        all recent articles topics
        and finds the most trending ones
        """
        pass

    def read_news(self):
        """
        Method that reads news
        and analyze the trending topics
        with the corresponding sentiment
        """
        pass

    # Fetches stock data through Oracles
    # Based on the news fetched
    def fetch_stock_data(self):
        pass
    
    # Exchange stocks based on the stock data
    def exchange(self):
        pass
    
    # Monitor performance of the trader
    def monitor(self):
        pass

    # Report the performance of the trader
    def report(self):
        pass


if __name__ == "__main__":
    # Creating trader object, which will start to operate
    trader = Trader()
