from broker.broker import FTX




class Settings: 
    backtesting = False
    base_asset = 'USD'
    path = "ftx.key"
    broker = FTX()
    drawdown = 1 - 100/100
    risk = 1 - 100/100
    watchlist=[
            'BTC',
            ]
    fee = 0.07/100