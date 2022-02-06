import importlib


class Settings:

    def __init__(self) -> None:
        self.broker_name = 'ftx'

        if self.broker_name == 'ftx':
            self.ftx()
        elif self.broker_name == 'binance':
            self.binance()
            
        self.backtesting = False
        self.base_asset = 'USD'
        broker = getattr(importlib.import_module('Python_Brokers_API'), '%s'%self.broker_name)
        self.broker = broker()
        self.path = self.broker_name +".key"
        self.expected_yield = 1 + 0.1/100
        self.real_expected_yield = self.expected_yield + 2*self.fee 
        self.risk = 1 - 5/100
        self.program_risk = 10/100
        self.timeframe = 15
        self.prediction_time = 15
        
        
        
    def ftx(self):
        self.watchlist=[
            'BTC',
            ]  
        self.fee = 0.07/100
        

    def binance(self):
        self.watchlist=[
            'BTC','ETH',
            ]
        self.fee = 0.1/100
        