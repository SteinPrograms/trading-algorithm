"""SDK for the postgres database"""
from datetime import datetime

import os
import psycopg2

from bot_exceptions import DatabaseException
from logs import logger



class Database:
    """Database SDK"""
    def __init__(self):
        self.data = {}
        for attempts in range(10):
            try:
                self.conn = psycopg2.connect(
                        host="db",
                        database=os.getenv('POSTGRES_DB'),
                        user=os.getenv('POSTGRES_USER'),
                        password=os.getenv('POSTGRES_PASSWORD'),
                    )
                break
            except DatabaseException as error:
                logger.error('Could not connect to database %s',error)
                if attempts==9:
                    raise error

    def select(
            self,
            *,
            query: str,
        ):
        """Select data from the database"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall().copy()
        self.conn.close()
        return result

    def insert(
            self,
            *,
            query: str,
        ):
        """Insert a query into the database"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
        self.conn.commit()
        self.conn.close()

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


if __name__ == "__main__":
    Database().add_position(
        time=datetime.now(),
        symbol="BTC/USD",
        yield_value='2.31%',
        wallet_value='1,000,000.00$',
    )
    print(Database().select(
        query="SELECT * FROM positions",
    ))
