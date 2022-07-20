"""Global Settings"""

import os
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
broker = FTX(
                api_key= os.getenv('BROKER_API'),
                api_secret= os.getenv('BROKER_SECRET'),
)
