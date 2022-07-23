"""Python testing module"""
from collections import deque
import numpy as np
from datetime import datetime,timedelta

from app.local_websocket.websocket_client import FtxWebsocketClient


websocket = FtxWebsocketClient()

def metrics(trades:deque):
    """Gives volatilty for deque"""
    prices = [trade['last'] for trade in trades]
    return prices[-1]/prices[0]

class History:
    values = deque(maxlen=50000)

    def get_sorted_increased_history(self):
        return sorted([value for value in self.values if value>1])
    
    def get_sorted_decreased_history(self):
        return sorted([value for value in self.values if value<1])

    def get_highest_increase(self):
        history = self.get_sorted_increased_history()
        return history[int((len(history)-1)*0.95)]
    
    def get_highest_decrease(self):
        history = self.get_sorted_decreased_history()
        return history[int((len(history)-1)*0.05)]


SYMBOL = "BTC/USD"
DATA_LENGTH = 50
history = History()
last_X_trades = deque(maxlen=DATA_LENGTH)



while True:
    previous_data  = websocket.get_ticker(SYMBOL).copy()
    if 'bid' in previous_data:
        previous_data.pop("time")
        break

while True:
    current_data = websocket.get_ticker(SYMBOL).copy()
    if 'bid' in current_data:
        current_data.pop("time")
        if previous_data.get("last") != current_data.get("last"):
            last_X_trades.append(current_data)
            previous_data = current_data
            # fully loaded
            if len(last_X_trades)==DATA_LENGTH:
                metric = metrics(last_X_trades)
                try:
                    # current positive gap is stronger the usual one => Strong buys
                    if metric > history.get_highest_increase() and len(history.values)>100:
                        print("buy")
                    # current negative gap is stronger the usual one => Strong sells
                    elif metric < history.get_highest_decrease() and len(history.values)>100:
                        print("sell")
                    else:
                        print("hodle")
                except IndexError:
                    pass
                history.values.append(metrics(last_X_trades))
                print(history.get_sorted_increased_history())
