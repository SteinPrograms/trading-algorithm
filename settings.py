import importlib


class Settings:
    """

    """

    def __init__(self) -> None:
        self.broker_name = 'binance'
        self.program_version = 'v0.1_MeanTrading'
        self.username = 'Hugo'
        self.commentaire =r"Test en gardant les 50% plus grands écarts, et correction du bug d'enregistrement et possibilité d'arreter le programme manuellement"
        
        
        if self.broker_name == 'ftx':
            self.ftx()
        elif self.broker_name == 'binance':
            self.binance()
            
        self.program_name = self.program_version+'_'+self.username+'_'+self.broker_name
        self.backtesting = False
        self.base_asset = 'USDT'
        broker = getattr(importlib.import_module('Python_Brokers_API'), '%s'%self.broker_name)
        self.broker = broker()
        self.path = self.broker_name +".key"
        self.expected_yield = 1 + 2*self.fee 
        self.risk = 1 - 5/100
        self.program_risk = 10/100
        
        
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
        

    def parameters(self,):
        pass