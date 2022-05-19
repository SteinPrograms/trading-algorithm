
    
    
from settings import Settings
from database import Database

def mean(array : list)->float:
    return sum(array)/len(array)


class Prediction:
    def __init__(self):
        pass

    def signal(self,symbol:str) ->dict[str]:
        currentPrice = Settings().broker.price(symbol)["bid"]
        if round(currentPrice/100,0)==round(Database().get_target_value(symbol)/100,0):
            return {"signal":"buy",
                    "yield":Database().get_expected_yield(symbol) - 2 * Settings().fee,
                    }
        else:
            return {"signal":"neutral"}
        
        
if __name__ == "__main__":
    print(Prediction().request_entry_price("ETH/USD"))