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

import os
from binance.spot import Spot
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

client = Spot()

# # Get server timestamp
# print(client.time())


data = client.klines("ETHUSDC", "1m", limit=1440)
pprint(data)

pprint(len(data))

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
# - Moving average
# - RSI
# - MACD
# - Bollinger bands
# - Ichimoku cloud

# Let's start with moving average
# - Buy when the price is above the moving average
# - Sell when the price is below the moving average

def moving_average_strategy(historical_data, period):
    """Moving average strategy
    Calculate the moving average of the last period
    """
    # Get the opening and closing price
    number_of_winning_trades = 0
    number_of_trades = 0
    results = list()


    # Convert data to float
    historical_data = [[float(element) for element in data] for data in historical_data]



    for index,current_data in enumerate(historical_data):
        opening_price = current_data[1]
        if index < period:
            continue
        try:
            moving_average = sum([data[4] for data in historical_data[index-period:index]]) / period
        except:
            continue
        
        # Identify entry points
        if opening_price > moving_average:
            # Buy
            future_historical_data = historical_data[index+1:]
            # Identify exit points
            for future_index,future_data in enumerate(future_historical_data):
                future_opening_price = future_data[1]

                new_moving_average = sum([data[4] for data in historical_data[(index+future_index)-period:(index+future_index)]]) / period
                if future_opening_price < new_moving_average:
                    # Sell
                    # Calculate profit percentage
                    profit_percentage = (future_opening_price - opening_price) / opening_price * 100
                    # Calculate drawdown
                    if future_index == 0:
                        future_lowest_price = future_data[3]
                    else:
                        future_lowest_price = min([data[3] for data in future_historical_data[0:future_index]])
                    drawdown = (future_lowest_price - opening_price) / opening_price * 100
                    # Leave position loop
                    results.append(
                        {
                            "profit_percentage": profit_percentage,
                            "drawdown": drawdown,
                            "position_time": future_index,
                            "error":False,
                        }
                    )
                    break

                if future_index == len(future_historical_data) - 1:
                    print("ERROR : Didn't sell")
                    # If we arrive here, it means that we didn't sell
                    # Make the position in error.
                    results.append(
                        {
                            "profit_percentage": 0,
                            "drawdown": 0,
                            "position_time": 0,
                            "error":True,
                        }
                    )
    
    return results


# Identify best moving average period
for period in range(10, 100):
    print(f"Period: {period}")
    results = moving_average_strategy(data, period)
    print(f"Number of trades: {len(results)}")
    if len(results) == 0:
        continue

    total_profit_percentage = sum([result["profit_percentage"] for result in results if result["error"]==False])
    average_profit_percentage = total_profit_percentage / len(results)
    print(f"Average profit percentage: {average_profit_percentage}")
    total_drawdown = sum([result["drawdown"] for result in results if result["error"]==False])
    average_drawdown = total_drawdown / len(results)
    print(f"Average drawdown: {average_drawdown}")

# pprint(moving_average_strategy(data, 10))

# Read API keys from environment variables
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')

# API key/secret are required for user data endpoints
client = Spot(api_key=api_key, api_secret=api_secret)
