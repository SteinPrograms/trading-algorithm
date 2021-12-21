import os,time,re
from settings import Settings

class RealCommands:
    def __init__(self) -> None:
        self.broker = Settings().broker
        path = Settings().path
        if os.path.exists(path) == False:
            print("YOU MUST CREATE KEY FILE")
            self.create_key_file()
        self.broker.connect_key(path)

    def test_connection(self,):
        return self.broker.test_order()

    def create_key_file(self): 
        API_KEY = str(input("Enter your API key :"))
        SECRET_KEY = str(input("Enter your SECRET_KEY :"))
        with open(Settings().path,"w") as file:
            file.write(API_KEY+'\n')
            file.write(SECRET_KEY)


    def limit_close(self,symbol,backtesting):
        #Checking connectivity
        print("checking connectivity")
        if not backtesting:
            while True:
                try:
                    #Get the quantity of crypto in balance
                    balance = self.broker.get_balances(re.sub("[^0-9a-zA-Z]+", "", symbol.replace(Settings().base_asset,'')))
                    quantity = float(balance['free'])
                    break
                except:
                    time.sleep(0.2)
            print("Creating sell order")
            counter=0
            while(True):
                try:
                    #Create the sell order with the whole quantity of asset
                    order = self.broker.create_market_order(
                        symbol=symbol,
                        side='sell',
                        quantity=quantity,
                        )
                    #We test if there is a code error
                    print("SellingOrderApproval",order["msg"])
                    time.sleep(0.2)
                    counter+=1
                    if counter ==10:
                        return {'error':True}
                except:
                    break

            #Now wait for the order to be filled.
            while(True):
                try:
                    print("Waiting for the order to be filled")
                    #Get the quantity of fiat in balance
                    while(True):
                        try:
                            #Get the quantity of fiat in balance
                            balance = self.broker.get_balances(Settings().base_asset)
                            quantity = float(balance['free'])
                            break
                        except Exception as error:
                            print(error)
                            time.sleep(1)
                    #If we have recovery of fiat balance then it means sell is ok
                    if quantity > 10:
                        print("Order filled")
                        break
                    time.sleep(0.2)
                except:
                    pass

            return order

    def limit_open(self,symbol,backtesting):
        #Checking connectivity
        if backtesting:
            return

        print("getting the balance...")
        while(True):
            try:
                #Get the quantity of fiat in balance
                balance = self.broker.get_balances(Settings().base_asset)
                quantity = float(balance['free'])
                break
            except Exception as error:
                print(error)
                time.sleep(0.2)

        print("Creating buy order...")
        counter=0
        while(True):
            try:
                #Create the buy order with the whole quantity you can buy with balance
                buy_order = self.broker.create_market_order(
                    symbol=symbol,
                    side='buy',
                    quantity=quantity,
                    )
                #We test if there is a code error
                print("BuyOrderApproval",buy_order["msg"])
                time.sleep(0.2)
                counter+=1
                if counter ==10:
                    return {'error':True}
            except:
                break

        print("Waiting for the order to be filled")
        #Now wait for the order to be filled.
        while(True):
            try:
                
                while(True):
                    try:
                        #Get the quantity of fiat in balance
                        balance = self.broker.get_balances(Settings().base_asset)
                        quantity = float(balance['free'])
                        break
                    except Exception as error:
                        print(error)
                        time.sleep(0.2)
                if quantity < 10:
                    print("Order filled")
                    break
            except:
                pass

        return {'error':False,'order':buy_order}
