from settings import Settings
from csv import DictWriter

data = Settings().broker.get_historical_prices("ETH/USD")



with open('spreadsheet.csv','w') as outfile:
    writer = DictWriter(outfile, data[0].keys())
    writer.writeheader()
    writer.writerows(data)