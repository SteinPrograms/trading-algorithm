from broker import FTX

BACKTESTING = False
BASE_ASSET = 'USD'
PATH = "ftx.key"
DRAWDOWN = 0
RISK = 0
FEE = 0.07/100
WATCH_LIST=[
        'BTC',
]
broker = FTX()