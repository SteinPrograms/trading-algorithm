import importlib


class Settings:
    def __init__(self) -> None:
        self.fee = 0.07 / 100
        self.broker_name = 'ftx'
        self.program_version = 'v0.0'
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
        self.timeframe = 15
        self.prediction_time = 15
