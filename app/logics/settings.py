from app.broker.broker import FTX




class Settings:
    def __init__(self) -> None:
        self.backtesting = False
        self.base_asset = 'USD'
        self.path = "ftx.key"
        self.broker = FTX()
        self.drawdown = 1 - 100/100
        self.risk = 1 - 100/100
        self.watchlist=[
            'BTC',
            ]
        self.fee = 0.07/100