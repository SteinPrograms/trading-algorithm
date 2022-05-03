import pymongo


class Database:
    def __init__(self):
        password = "Manonhugo147"
        username = "hugodemenez"
        uri = f"mongodb+srv://{username}:{password}@test.yqzxd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(uri)
        
    def get_target_value(self,symbol:str) -> float:
        db = self.client.Trading
        try:
            return float(db.Target.find_one({"symbol":symbol})['target'])
        except Exception:
            return 0.0
        
    def get_expected_yield(self,symbol:str) -> float:
        db = self.client.Trading
        try:
            return float(db.Target.find_one({"symbol":symbol})['yield'])
        except Exception:
            return 0.0