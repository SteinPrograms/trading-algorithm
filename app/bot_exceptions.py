"""Module defining exceptions"""

class DrawdownException(Exception):
    """Exception raised on drawdown exceed"""

class ServerStopException(Exception):
    """Exception raised on Server stop"""

class WebsocketException(Exception):
    """Exception raised on websocket connection exception"""

class NullBalanceException(Exception):
    """Exception raised on balance fetched 0"""

class BrokerConnectionException(Exception):
    """Exception raised on broker connection error"""

class OrderException(Exception):
    """Exception raised on order error"""

class DatabaseException(Exception):
    """Exception raised on database error"""
