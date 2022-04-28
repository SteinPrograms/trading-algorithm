from broker import FTX
class Settings:

    def __init__(self) -> None:
        self.backtesting = False
        self.base_asset = 'USD'

        self.broker = broker()
        self.path = f'{self.broker_name}.key'
        self.expected_yield = 1 + 0.05/100
        self.real_expected_yield = self.expected_yield + 2*self.fee
        self.risk = 1 - 5/100
        self.program_risk = 10/100
        self.timeframe = 30
        self.prediction_time = 15 # It is the expected time in position to collect the expected yield
        
        
        
    def ftx(self):
        self.watchlist=[
            'BTC',
            ]  
        self.fee = 0.07/100
        
        