"""Module SDK to pass orders to FTX market"""
import time
import re
import settings
from bot_exceptions import NullBalanceException, BrokerConnectionException, OrderException
from logs import logger

class RealCommands:
    """Class SDK for broker connection"""
    def __init__(self) -> None:
        self.broker = settings.broker

    def test_connection(self,):
        """Test the connection with the broker using API and SECRET"""
        return self.broker.test_order()

    def get_order_status(self,order_id):
        """Get the order status JSON with order_id as param"""
        return self.broker.get_order_status(order_id)

    def get_quantity_crypto(self,symbol):
        """
        Retrive the quantity of crypto in the balance
        retries every sec until it gets it
        """
        while True:
            try:
                # Get the quantity of crypto in balance
                quantity = float(
                    self.broker.get_balances(
                        re.sub("[^0-9a-zA-Z]+", "", symbol.replace(settings.BASE_ASSET,''))
                    ).get("free",None)
                )
                break
            except BrokerConnectionException:
                time.sleep(0.2)
        return quantity

    def get_quantity_fiat(self):
        """
        Retrive the quantity of fiat in the balance
        retries every sec until it gets it
        """
        while True:
            try:
                # Get the quantity of fiat in balance
                quantity = float(self.broker.get_balances(settings.BASE_ASSET)['free'])
                break
            except BrokerConnectionException:
                time.sleep(1)
        return quantity

    def market_close(self,symbol,backtesting):
        """Creating a close order at market price"""
        # Checking connectivity
        logger.info("checking connectivity")
        # Checking backtesting mode
        if not backtesting:
            # Getting quantity of free balance
            quantity_crypto = self.get_quantity_crypto(symbol)

            logger.info("Creating sell order")
            # Initializing counter to overcome order issues
            counter=0
            while True:
                try:
                    logger.info("Attempt n° : %s",counter)
                    # Create the sell order with the whole quantity of asset
                    order = self.broker.place_order(symbol,"sell",0,quantity_crypto,'market')
                    if not "msg" in order:
                        # If there is no msg it means the order is sent
                        logger.info("SellingOrderApproval %s",order)
                        raise OrderException()
                    time.sleep(0.2)
                    counter+=1
                    if counter ==10:
                        return {'error':True}
                except OrderException:
                    break

            # Now wait for the order to be filled.
            while(True):
                logger.info("Waiting for the order to be filled")
                quantity_fiat = self.get_quantity_fiat()
                ### Get here once fiat balance is successfully retrieved

                # If we have at least 20 $ free of fiat balance then it means sell is executed
                if quantity_fiat > 20:
                    logger.info("Order filled")
                    break

                ### Else it means the order is not executed yet
                time.sleep(0.2)
            return {'error':False,'order':order}

    def market_open(self,symbol,backtesting):
        """Creating a open order at market price"""
        # Checking connectivity
        if backtesting:
            return

        logger.info("getting the balance...")

        quantity_fiat = self.get_quantity_fiat()

        logger.info("Creating buy order...")
        for error_counter in range(10):
            # Create the buy order with
            # the whole quantity you can buy with balance - 5$ (for slippage prevention)
            # TODO find a way to use the full balance
            try:
                order = self.broker.place_order(
                    symbol,
                    "buy",
                    0,
                    (quantity_fiat-5)/self.broker.price(symbol)['bid'],
                    'market',
                    )

            except OrderException as error:
                logger.info(error)

            # We test if there is a code error
            if not "msg" in order:
                break

            # If there is a code error, we log it and retry in 0.2s
            logger.info("BuyOrderApproval",order["msg"])
            time.sleep(0.2)

            # If we exceed the maximum attempts without getting order approval
            # leave the method with error code
            if error_counter == 9:
                return {'error':True}

        logger.info("Waiting for the order to be filled")
        # Now wait for the order to be filled.
        while True:
            quantity_fiat = self.get_quantity_fiat()
            if quantity_fiat < 20:
                logger.info("Order filled")
                break
        return {'error':False,'order':order}

    def balance_check(self) -> float:
        """Checking if balance is above X"""
        logger.info("getting the balance...")
        while True:
            try:
                # Get the quantity of fiat in balance
                balance = self.broker.get_balances(settings.BASE_ASSET)
                quantity = float(balance['free'])
                # It is ok if quanity is high enough
                if quantity > 20:
                    return quantity
                raise NullBalanceException("Balance is currently null")

            except Exception as error:
                logger.info(error)
                time.sleep(0.2)

if __name__ == '__main__':
   #logger.info(RealCommands().broker.place_order("BTC/USD","sell",0,0.000556,'market'))
    # Testing brokerconnection with buy/sell orders
    logger.info(RealCommands().market_open("BTC/USD",False))
    logger.info(RealCommands().market_close("BTC/USD",False))
