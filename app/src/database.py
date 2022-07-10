from datetime import datetime
import logging,psycopg2,os
from routine import Routine


class Database:
    def __init__(self):
        print(f"""
        Trying to connect to {os.getenv('POSTGRES_DB')} 
        as {os.getenv('POSTGRES_USER')} 
        with password {os.getenv('POSTGRES_PASSWORD')}
        """)
        self.conn = psycopg2.connect(
            host="localhost",
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )

    def select(self,*,query: str):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            print(cursor.fetchall())
        self.conn.close()

    def insert(self,*,query: str):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
        self.conn.commit()
        self.conn.close()

    def add_position(self,*,time,symbol,yield_value,wallet_value):
        self.insert(query=f"INSERT INTO positions(time,symbol,yield,wallet_value) values('{time}','{symbol}','{yield_value}','{wallet_value}')")



"""
Test script
"""

if __name__ == "__main__":
    from datetime import datetime
    import time
    Database().add_position(time=datetime.now(),symbol="BTC/USD",yield_value='2.31%',wallet_value='1,000,000.00$')
    Database().select(query="SELECT * FROM positions")