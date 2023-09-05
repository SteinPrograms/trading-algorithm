import requests
from datetime import datetime
from statistics import mean
import logging

class Indicator:
    """
    Indicator of technical analysis
    """
    def __init__(self):
        self.signal = 'initialize'
    
    def get_klines(self,symbol):
        """
        Get latest klines from binance API

        Returns:
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
            logging.warning(f"Error {klines.status_code} while getting klines")
            return
        return klines.json()

    def sma(self,klines:list,length:int):
        """
        Computes a simple moving average
        which is a sum of the last n prices divided by n
        """
        sma = 0
        for i in range(length):
            sma += float(klines[-i-1][4])
        return sma/length

    def stdev(self,klines:list,length:int):
        """
        Computes standard deviation
        which is the square root of the variance (which is the average of the squared differences from the mean)
        """
        sma = self.sma(klines,length)
        stdev = 0
        for i in range(length):
            stdev += (float(klines[-i-1][4]) - sma)**2
        return (stdev/length)**0.5

    def rsi(self,klines:list,length:int):
        """
        compute relative strength index
        which is the average of the gains over the average of the losses
        """
        up = list()
        down = list()
        for i in range(length):
            variation = float(klines[-i-1][4]) - float(klines[-i-2][4])
            if variation >= 0:
                up.append(variation)
                down.append(0)
            else:
                down.append(-variation)
                up.append(0)
            
            average_gain = mean(up)
            average_loss = mean(down)

        return 100 - (100/(1+average_gain/average_loss))

    def get_signal(self,symbol:str):
        """

        """

        klines = self.get_klines(symbol)

        rsi = self.rsi(klines,14)

        self.close = float(klines[-1][4])
        upper = self.sma(klines,20) + 2 * self.stdev(klines, 20)
        lower = self.sma(klines,20) - 2 * self.stdev(klines, 20)
        middle = self.sma(klines,20)
        
        try:
            # Upper
            crosses_above_upper = self.was_below_upper and self.close >= upper
            crosses_below_upper = self.was_above_upper and self.close <= upper

            # Lower
            crosses_below_lower = self.was_above_lower and self.close <= lower
            crosses_above_lower = self.was_below_lower and self.close >= lower

            # Middle
            crosses_below_middle = self.was_above_middle and self.close <= middle
            crosses_above_middle = self.was_below_middle and self.close >= middle


            if crosses_above_lower and rsi < 30:
                self.signal = 'buy'
            else:
                self.signal = 'neutral'

            if crosses_below_upper and rsi > 70:
                self.signal = 'sell'

        except:
            pass
        

        self.was_below_upper = self.close < upper
        self.was_above_upper = self.close > upper
        self.was_below_lower = self.close < lower
        self.was_above_lower = self.close > lower
        self.was_below_middle = self.close < middle
        self.was_above_middle = self.close > middle
