from broker import FTX




class Settings:
    def __init__(self) -> None:
        self.backtesting = False
        self.base_asset = 'USD'
        self.path = "ftx.key"
        self.broker = FTX()
        self.drawdown = 1 - 20/100
        self.risk = 1 - 5/100
        self.watchlist=[
            'BTC',
            ]
        self.fee = 0.07/100
        self.expected_yield = 1 + 0.3/100 + 2*self.fee