import logging,psycopg2,os
from routine import Routine

class Levels:
    def update(self,data:dict) :
        try:
            self._yield = data['yield']
            self._entry_price = data['target']
        except Exception as error:
            logging.error(error)

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="trading",
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
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
        try:	
            # create a cursor
            cur = self.conn.cursor()
            
            cur.execute('SELECT version()')

            db_version = cur.fetchone().copy()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return db_version