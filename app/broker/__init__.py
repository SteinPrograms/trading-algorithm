"""Brokerage connection module
"""


import os
from dotenv import load_dotenv
from binance.spot import Spot

load_dotenv()

# Read API keys from environment variables
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')
# API key/secret are required for user data endpoints
client = Spot(api_key=api_key, api_secret=api_secret)