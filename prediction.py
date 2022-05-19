from settings import Settings
from database import Database

class Prediction:
    def __init__(self):
        pass

    def scalping(self,symbol:"LUNA/USD",):
        values = Settings().broker.get_historical_data(symbol,60)

        average_yield = [value['close'] for value in values]
        
        
        hourly_yield = [average_yield[i+120]/average_yield[i]-1 for i in range(0,round(len(average_yield)/120)-1,120)]
        
        
        
        return {
            'is_min':min(value['close'] for value in values)>values[-1]['close'],
            'yield':(sum(hourly_yield)/len(hourly_yield))
            }
        
    def signal(self,symbol:str) ->dict[str]:
        scalping = self.scalping(symbol)
        if scalping['is_min'] and scalping['yield']>0.0014:
            return {"signal":"buy",
                    "yield":scalping['yield'] - 2 * Settings().fee,
                    }
        else:
            return {"signal":"neutral"}
        
        
if __name__ == "__main__":
    print(Prediction().scalping("LUNA/USD"))