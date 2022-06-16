import logging,pymongo
from routine import Routine

class Levels:
    def __init__(self,):
        pass

    def update(self,data:dict) :
        try:
            self._yield = data['yield']
            self._entry_price = data['target']
        except Exception as error:
            logging.error(error)

class Database:
    def __init__(self):
        password = "Manonhugo147"
        username = "hugodemenez"
        self.uri = f"mongodb+srv://{username}:{password}@test.yqzxd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        self.send_program_data()
        self._server_data = {}
        self.levels = Levels()

    def update_server_data(self,data):
        for key in data.keys():
            self._server_data[key] = data[key]

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

    @Routine(10)
    def fetch_and_update_database_data(self):
        """Routine to :
            - update program data to db
            - update position data to db
            - get new levels from db"""
        with pymongo.MongoClient(self.uri) as client:
            try:
                client.Trading.Server.update_one(filter={},update={'$set':self._server_data},upsert=True)
            except Exception as error:
                logging.error(error)
            try:
                self._levels.update(client.Trading.Target.find_one({}))
            except Exception as error:
                logging.error(error)
            
