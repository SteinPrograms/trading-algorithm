import requests
from datetime import datetime
class Prediction:
    """Class used to predict buy actions"""
    def __init__(self):
        pass
    
    def get_klines(self,symbol):
        """
        [
            [
                1499040000000,      // Kline open time
                "0.01634790",       // Open price
                "0.80000000",       // High price
                "0.01575800",       // Low price
                "0.01577100",       // Close price
                "148976.11427815",  // Volume
                1499644799999,      // Kline Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "0"                 // Unused field, ignore.
            ]
        ]
        """
        klines = requests.get('https://data-api.binance.vision/api/v3/klines',params={
            'symbol':symbol,
            'interval':'1h'
        })
        if klines.status_code != 200:
            Log(f"Error {klines.status_code} while predicting")
            return
        return klines.json()

    def sma(self,klines:list,length:int):
        """
        klines = [
            [
                1499040000000,      // Kline open time
                "0.01634790",       // Open price
                "0.80000000",       // High price
                "0.01575800",       // Low price
                "0.01577100",       // Close price
                "148976.11427815",  // Volume
                1499644799999,      // Kline Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "0"                 // Unused field, ignore.
            ]
        ]
        """
        sma = 0
        for i in range(length):
            sma += float(klines[-i-1][4])
        return sma/length

    def stdev(self,klines:list,length:int):
        """
        klines = [
            [
                1499040000000,      // Kline open time
                "0.01634790",       // Open price
                "0.80000000",       // High price
                "0.01575800",       // Low price
                "0.01577100",       // Close price
                "148976.11427815",  // Volume
                1499644799999,      // Kline Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "0"                 // Unused field, ignore.
            ]
        ]
        """
        sma = self.sma(klines,length)
        stdev = 0
        for i in range(length):
            stdev += (float(klines[-i-1][4]) - sma)**2
        return (stdev/length)**0.5

    def signal(self,symbol:str):
        """Give the buy signal

        Args:
        """

        klines = self.get_klines(symbol)

        close = float(klines[-1][4])
        upper = self.sma(klines,20) + 2 * self.stdev(klines, 20)
        lower = self.sma(klines,20) - 2 * self.stdev(klines, 20)
        middle = self.sma(klines,20)

        try:
            # Upper
            if self.was_below_upper and close >= upper:
                crosses_above_upper = True
            else:
                crosses_above_upper = False
            if self.was_above_upper and close <= upper:
                crosses_below_upper = True
            else:
                crosses_below_upper = False

            # Lower
            if self.was_above_lower and close <= lower:
                crosses_below_lower = True
            else:
                crosses_below_lower = False
            if self.was_below_lower and close >= lower:
                crosses_above_lower = True
            else:
                crosses_above_lower = False

            # Middle
            if self.was_above_middle and close <= middle:
                crosses_below_middle = True
            else:
                crosses_below_middle = False
            if self.was_below_middle and close >= middle:
                crosses_above_middle = True
            else:
                crosses_above_middle = False

            if crosses_above_lower:
                return 'buy'

            if crosses_above_upper:
                return 'sell'
        except:
            pass
        

        self.was_below_upper = close < upper
        self.was_above_upper = close > upper
        self.was_below_lower = close < lower
        self.was_above_lower = close > lower
        self.was_below_middle = close < middle
        self.was_above_middle = close > middle


if __name__ == "__main__":
    predictor = Prediction()

    predictor.signal('BTCUSDT')
