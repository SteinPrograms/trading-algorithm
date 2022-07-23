"""SDK for the postgres database"""

import os
import psycopg2
import psycopg2.extras
from bot_exceptions import DatabaseException
from routine import Routine
from logs import logger

# DEV ENV
try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
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
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            ) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
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
            host=os.getenv('POSTGRES_HOST'),
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
        try:
            for data, value__ in data.items():
                self.data[data] = value__
        except RuntimeError:
            # Could be raised if data is changed during update
            pass

    @Routine(1)
    def routine_server_data_update(self):
        """Update server data very 5sec"""
        self.insert(
            query=""
            "INSERT INTO server("
            "id,"
            "current_status,"
            "total_yield,"
            "running_time,"
            "symbol,"
            "current_position_time,"
            "current_price,"
            "open_price,"
            "current_yield"
            ") values("
            "'1',"
            f"'{self.data.get('current_status','close')}',"
            f"{self.data.get('total_yield',1)},"
            f"'{self.data.get('running_time')}',"
            f"'{self.data.get('symbol',None)}',"
            f"'{self.data.get('current_position_time',None)}',"
            f"{self.data.get('current_price',0)},"
            f"{self.data.get('open_price',0)},"
            f"{self.data.get('current_yield',0)}"
            ") "
            "ON CONFLICT (id) DO UPDATE "
            f"SET "
            f"current_status = '{self.data.get('current_status')}', "
            f"total_yield = {self.data.get('total_yield',1)}, "
            f"running_time = '{self.data.get('running_time')}', "
            f"symbol='{self.data.get('symbol',None)}',"
            f"current_position_time='{self.data.get('current_position_time',None)}',"
            f"current_price={self.data.get('current_price',0)},"
            f"open_price={self.data.get('open_price',0)},"
            f"current_yield={self.data.get('current_yield',0)}"
            ";"
        )
