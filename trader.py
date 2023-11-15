import logging
import dotenv
import requests

# Creating trader class
class Trader:
    # Constructor for trader class without any parameters
    def __init__(self):
        # Loading environment variables
        dotenv.load_dotenv()
        # Setting up logger with timestamp
        logging.basicConfig(
            filename="trader.log", 
            level=logging.INFO,
            format="%(asctime)s %(message)s"
        )
        # Creating logger object
        self.logger = logging.getLogger(__name__)

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
    def exchange(self, from_asset, to_asset, amount):
        # Get server time
        server_time = requests.get("https://api.kraken.com/0/public/Time")
        if (server_time.status_code == 200):
            if (server_time.json()["error"] == []):
                self.logger.info("Server time fetched successfully")
            else:
                self.logger.error(
                        "Error fetching server time due to internal API error"
                        f"Error: {server_time.json()['error']}"
                )
            print(server_time.json())
        else:
            self.logger.error("Error fetching server time due to request error")
    
    # Monitor performance of the trader
    def monitor(self):
        pass

    # Report the performance of the trader
    def report(self):
        pass


if __name__ == "__main__":
    # Creating trader object, which will start to operate
    trader = Trader()
    trader.exchange("BTC", "ETH", 100)
