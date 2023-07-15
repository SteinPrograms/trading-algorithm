"""SDK for the postgres database"""

from datetime import datetime

import os
import time
import psycopg2
import psycopg2.extras
from bot_exceptions import DatabaseException
from routine import Routine

class Database:
    """Database SDK"""
    def __init__(self):
        self.data = {}

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

    def save_position(
            self,
            *,
            opening_date: str,
            closing_date: str,
            symbol :str,
            yield_value : float,
            wallet_value : float,
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
            for content, _value in data.items():
                self.data[content] = _value
        except RuntimeError:
            # Could be raised if data is changed during update
            pass

