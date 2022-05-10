import requests,json


class Database:
    def __init__(self):
        #self.endpoint = "http://hugodemenez.fr/api/"
        self.endpoint = "http://localhost:3000/api/"
        
    def get_target_value(self,symbol:str) -> float:
        
        try:
            return float(requests.get(f"{self.endpoint}{symbol}").json()['target'])
        except Exception:
            return 0.0
        
    def get_expected_yield(self,symbol:str) -> float:
        try:
            return float(requests.get(f"{self.endpoint}{symbol}").json()['yield'])
        except Exception:
            return 0.0
        
    def publish_server_data(self,data:dict) -> int:
        response = requests.post(f"{self.endpoint}serverData",data=data)
        return response.status_code
        
        

print(Database().publish_server_data({'test':"test"}))