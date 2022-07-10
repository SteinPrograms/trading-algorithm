import os,time,re
import settings
from botExceptions import NullBalanceException

class RealCommands:
    def __init__(self) -> None:
        self.broker = settings.broker
        path = settings.path
        if os.path.exists(path) == False:
            print("YOU MUST CREATE KEY FILE")
            self.broker.create_key_file()
        self.broker.connect_key(path)

    def test_connection(self,):
        return self.broker.test_order()

    def get_order_status(self,id):
        return self.broker.get_order_status(id)

    def get_quantity_crypto(self,symbol):
        """
        Retrive the quantity of crypto in the balance
        retries every sec until it gets it
        """
        while True:
            try:
                # Get the quantity of crypto in balance
                quantity = float(self.broker.get_balances(re.sub("[^0-9a-zA-Z]+", "", symbol.replace(settings.base_asset,''))).get("free",None))
                break
            except Exception:
                time.sleep(0.2)
        return quantity

    def get_quantity_fiat(self):
        """
        Retrive the quantity of fiat in the balance
        retries every sec until it gets it
        """
        while(True):
            try:
                # Get the quantity of fiat in balance
                quantity = float(self.broker.get_balances(settings.base_asset)['free'])
                break
            except Exception as error:
                print(error)
                time.sleep(1)
        return quantity

    def limit_close(self,symbol,backtesting):
        # Checking connectivity
        print("checking connectivity")
        # Checking backtesting mode
        if not backtesting:
            # Getting quantity of free balance
            quantity_crypto = self.get_quantity_crypto(symbol)
            
            print("Creating sell order")
            # Initializing counter to overcome order issues
            counter=0
            while(True):
                try:
                    print(f"Attempt n° : {counter}")
                    # Create the sell order with the whole quantity of asset
                    order = self.broker.place_order(symbol,"sell",0,quantity_crypto,'market')
                    # If there is no msg it means the order is sent
                    print("SellingOrderApproval",order["msg"])
                    time.sleep(0.2)
                    counter+=1
                    if counter ==10:
                        return {'error':True}
                except Exception:
                    break

            # Now wait for the order to be filled.
            while(True):
                print("Waiting for the order to be filled")
                quantity_fiat = self.get_quantity_fiat()
                ### Get here once fiat balance is successfully retrieved

                # If we have at least 20 $ free of fiat balance then it means sell is executed
                if quantity_fiat > 20:
                    print("Order filled")
                    break

                ### Else it means the order is not executed yet
                time.sleep(0.2)                    
            return {'error':False,'order':order}

    def limit_open(self,symbol,backtesting):
        # Checking connectivity
        if backtesting:
            return

        print("getting the balance...")

        quantity_fiat = self.get_quantity_fiat()

        print("Creating buy order...")
        counter=0
        while True:
            try:
                # Create the buy order with the whole quantity you can buy with balance - 5$ (for slippage prevention) 
                # TODO find a way to use the full balance
                try:
                    order = self.broker.place_order(symbol,"buy",0,(quantity_fiat-5)/self.broker.price(symbol)['bid'],'market')

                except Exception as error:
                    print(error)

                #We test if there is a code error  
                print("BuyOrderApproval",order["msg"])
                time.sleep(0.2)
                counter+=1
                if counter ==10:
                    return {'error':True}
            except Exception:
                break

        print("Waiting for the order to be filled")
        # Now wait for the order to be filled.
        while True:
            quantity_fiat = self.get_quantity_fiat()
            if quantity_fiat < 20:
                print("Order filled")
                break
        return {'error':False,'order':order}
    
    def balance_check(self) -> float:
        print("getting the balance...")
        while(True):
            try:
                # Get the quantity of fiat in balance
                balance = self.broker.get_balances(settings.base_asset)
                quantity = float(balance['free'])
                # It is ok if quanity is high enough
                if quantity > 20:
                    return quantity
                raise NullBalanceException("Balance is currently null")
                
            except Exception as error:
                print(error)
                time.sleep(0.2)

    

if __name__ == '__main__':
   #print(RealCommands().broker.place_order("BTC/USD","sell",0,0.000556,'market'))
    # Testing brokerconnection with buy/sell orders
    print(RealCommands().limit_open("BTC/USD",False))
    print(RealCommands().limit_close("BTC/USD",False))
    
    