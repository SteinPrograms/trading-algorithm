import importlib


class Settings:

    def __init__(self) -> None:
        self.watchlist = [
            'BTC',
        ]
        self.fee = 0.07 / 100
        self.broker_name = 'ftx'
        self.program_version = 'v0.1_MeanTrading'
        self.username = 'Hugo'
        self.program_name = self.program_version + '_' + self.username + '_' + self.broker_name
        self.back_testing = False
        self.base_asset = 'USDT'
        broker = getattr(importlib.import_module('Python_Brokers_API'), '%s' % self.broker_name)
        self.broker = broker()
        self.path = self.broker_name + ".key"
        self.expected_yield = 1 + 2 * self.fee
        self.risk = 1 - 5 / 100
        self.program_risk = 10 / 100

    def parameters(self, ):
        pass
