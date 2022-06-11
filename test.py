from websocket_client import FtxWebsocketClient
from time import sleep

if __name__ == '__main__':
    client = FtxWebsocketClient()
    client.get_ticker('BTC/USD')
    memory = 0
    while True:
        if 'bid' in client._tickers['BTC/USD'] and client._tickers['BTC/USD']['bid'] != memory:
            print(f"NEW VALUE :{client._tickers['BTC/USD']['bid']}")
            memory = client._tickers['BTC/USD']['bid']

