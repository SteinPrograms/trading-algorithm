import asyncio
import ccxt.async_support as ccxt

async def print_poloniex_ethbtc_ticker():
    ftx = ccxt.ftx()
    print(await ftx.fetch_ticker('ETH/BTC'))

asyncio.run(print_poloniex_ethbtc_ticker())


x