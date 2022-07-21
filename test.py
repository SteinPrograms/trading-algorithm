from time import sleep

from app.routine import Routine

from app.websocket.websocket_client import FtxWebsocketClient
import asyncio

class Testing:
    def __init__(self):
        _data = None
        self.send_program_data()

    @Routine(10)
    def send_program_data(self):
        print(self._data)

async def scrutting_price():
    await client._tickers['BTC/USD']['bid'] < 23900
    print("position opened")

if __name__ == '__main__':
    print("--------",scrutting_price())
    test = Testing()
    test._data = 'test'
    client = FtxWebsocketClient()
    client.get_ticker('BTC/USD')
    test._data = 'update'
    memory = 0
    while True:
        if 'bid' in client._tickers['BTC/USD'] and client._tickers['BTC/USD']['bid'] != memory:
            print(f"NEW VALUE :{client._tickers['BTC/USD']['bid']}")
            memory = client._tickers['BTC/USD']['bid']
