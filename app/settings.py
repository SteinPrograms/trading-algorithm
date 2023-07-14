"""Global Settings"""

import os



BACKTESTING = False
BASE_ASSET = 'USD'
DRAWDOWN = 0
RISK = 0
FEE = 0.07/100
EXPECTED_YIELD = 0.1/100
broker = FTX(
        api_key= os.getenv('BROKER_API'),
        api_secret= os.getenv('BROKER_SECRET'),
)
