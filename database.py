


"""
import requests,json

class Database:
    def __init__(self):
        self.endpoint = "http://hugodemenez.fr/api/"
        #self.endpoint = "http://localhost:3000/api/"
        
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
        try:
            requests.post(f"{self.endpoint}postServerData",data=data)
            
        except Exception as error:
            print(error)
            

    def get_server_data(self) -> dict:
        try:
            response = requests.get(f"{self.endpoint}getServerData")
            return response.json()
        
        except Exception:
            return {'total_yield':'0%'}
        
    def publish_position_data(self,data:dict) -> int:
        try:
            requests.post(f"{self.endpoint}postPositionData",data=data)
            
        except Exception as error:
            print(error)
"""


import pymongo

class Database:
    def __init__(self):
        password = "Manonhugo147"
        username = "hugodemenez"
        self.uri = f"mongodb+srv://{username}:{password}@test.yqzxd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

        
    def get_target_value(self,symbol:str) -> float:
        with pymongo.MongoClient(self.uri) as client:
            try:
                db = client.Trading
                return float(db.Target.find_one({"symbol":symbol})['target'])
            except Exception:
                return 0.0
        
    def get_expected_yield(self,symbol:str) -> float:
        with pymongo.MongoClient(self.uri) as client:
            try:
                db = client.Trading
                return float(db.Target.find_one({"symbol":symbol})['yield'])
            except Exception:
                return 0.0
        
    def publish_server_data(self,data:dict) -> int:
        with pymongo.MongoClient(self.uri) as client:
            try:
                db = client.Trading
                db.server.update_one(filter={},update={'$set':data},upsert=True)
            except Exception as error:
                print(error)

            

    def get_server_data(self) -> dict:
        with pymongo.MongoClient(self.uri) as client:
            try:
                db = client.Trading
                return db.server.find_one(filter={})
            
            except Exception as error:
                return error


    def publish_position_data(self,data:dict) -> int:
        with pymongo.MongoClient(self.uri) as client:
            try:
                db = client.Trading
                db.Positions.insert_one(data)
            except Exception as error:
                print(error)


print(Database().publish_position_data({'hugo':'man'}))