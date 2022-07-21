"""SDK for the postgres database"""
from datetime import datetime

import os
from time import sleep
import psycopg2
from bot_exceptions import DatabaseException
from routine import Routine
from logs import logger

# DEV ENV
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

class Database:
    """Database SDK"""
    def __init__(self):
        self.data = {}
        # start routine
        self.routine_server_data_update()

    def select(
            self,
            *,
            query: str,
        ):
        """Select data from the database"""
        with psycopg2.connect(
            host="db",
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall().copy()

        return result

    def insert(
            self,
            *,
            query: str,
        ):
        """Insert a query into the database"""
        with psycopg2.connect(
            host="db",
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
            conn.commit()

    def add_position(
            self,
            *,
            time,
            symbol,
            yield_value,
            wallet_value,
        ):
        """Add position data into database"""
        self.insert(
            query=("INSERT INTO positions(time,symbol,yield,wallet_value)"
            f"values('{time}','{symbol}','{yield_value}','{wallet_value}')"
        ))

    def get_server_data(
        self):
        """Get server data from database"""

        return self.select(
            query = "SELECT * FROM server"
        )

    def update_server_data(
            self,
            data: dict,
        ):
        """Update server data to the queue for routine database upload"""
        self.data = data

    @Routine(5)
    def routine_server_data_update(self):
        """Update server data very 5sec"""
        self.insert(
            query="INSERT INTO server(current_status,total_yield,running_time) values("
            f"'{self.data.get('current_status',None)}',"
            f"'{self.data.get('total_yield',None)}',"
            f"'{self.data.get('running_time',None)}'"
            ")"
        )


if __name__ == "__main__":
    Database()
    while True:
        pass
