"""
Backtesting algorithm
Finds best strategy based on previous data

1. Get data from binance
2. Create a strategy
3. Backtest the strategy
4. Get the results
5. Save the results
6. Repeat for all strategies
7. Get the best strategy
8. Save the best strategy
9. Run the best strategy
10. Save the results

"""

from pprint import pprint
from dotenv import load_dotenv
from binance.spot import Spot

load_dotenv()

client = Spot()

data = client.klines("ETHUSDC", "1m", limit=1440)

# Results :
# [
# # [
# #     1499040000000,      # Open time
# #     "0.01634790",       # Open price
# #     "0.80000000",       # High price
# #     "0.01575800",       # Low price
# #     "0.01577100",       # Close price
# #     "148976.11427815",  # Base asset volume
# #     1499644799999,      # Close time
# #     "2434.19055334",    # Quote asset volume
# #     308,                # Number of trades
# #     "1756.87402397",    # Taker buy base asset volume
# #     "28.46694368",      # Taker buy quote asset volume
# #     "0" # Ignore.
# # ]
# ]


# I need the opening and closing time, highest and lowest price
# Every position will be opened at an opening time. Due to lack of data;


# What type of strategy ?
# - Moving average (price crosses moving average, moving average crosses moving average)
# - RSI
# - MACD
# - Bollinger bands
# - Ichimoku cloud


class Strategies:
    """Strategies class"""

    def __init__(self,historical_data:list):
        self.historical_data = historical_data

    def __repr__(self) -> str:
        return (
            "Strategies restults : "
            f"{self.price_crossing_moving_average()}"
        )

    def convert_data_to_float(self,) -> list:
        """Convert all fields of historical data to float

        Returns:
            list: historical data with all fields converted to float
        """
        return [[float(element) for element in data] for data in self.historical_data]

    # Let's start with moving average
    # - Buy when the price is above the moving average
    # - Sell when the price is below the moving average
    def price_crossing_moving_average(self) -> dict:
        """Moving average strategy
        Calculate the moving average of the last period
        """

        historical_data = self.convert_data_to_float()

        # Store results
        results = []
        for period in range(10, 25):
            for opening_index,opening_data in enumerate(historical_data):
                opening_price = opening_data[1]
                # Prevents from getting out of range
                if opening_index < period:
                    # Go to next iteration
                    continue
                # Else we can calculate the moving average
                moving_average = sum(
                    data[4]
                    for data in historical_data[opening_index-period:opening_index]
                ) / period

                # If state is not defined, define it
                try:
                    state
                except UnboundLocalError:
                    state = "above" if opening_price > moving_average else "below"
                    continue

                # If just crosses the moving average (from below to above)
                if state == "below" and opening_price > moving_average:
                    # Identify exit points
                    for future_index,future_data in enumerate(historical_data[opening_index:]):
                        future_opening_price = future_data[1]
                        new_moving_average = sum(
                            data[4]
                            for data in historical_data[
                                # Recalculate the moving average for each new data
                                (opening_index+future_index)-period
                                :
                                (opening_index+future_index)
                            ]
                        ) / period

                        # If the price crosses
                        # the moving average from above to below (can't be the same candle)
                        if state == "above" and future_opening_price < new_moving_average:

                            future_lowest_price = min(
                                # Lowest prices
                                data[3]
                                for data in historical_data[
                                    opening_index:opening_index+future_index
                                ]
                            )

                            # Leave position loop
                            results.append(
                                {
                                    "profit_percentage": (
                                        future_opening_price - opening_price
                                    ) / opening_price * 100,
                                    "drawdown": (
                                        future_lowest_price - opening_price
                                    ) / opening_price * 100,
                                    "position_time": future_index,
                                    "error":False,
                                }
                            )
                            break

                        if future_index == len(historical_data[opening_index+1:]) - 1:
                            print("ERROR : Didn't sell")
                            # If we arrive here, it means that we didn't sell
                            # Make the position in error.
                            results.append(
                                {
                                    "error":True,
                                }
                            )

                        state = "above" if future_opening_price > new_moving_average else "below"

                state = "above" if opening_price > moving_average else "below"

        return results


# Identify best moving average period
print(Strategies(data).price_crossing_moving_average())
