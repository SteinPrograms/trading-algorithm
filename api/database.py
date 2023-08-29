"""SDK for the postgres database"""

from datetime import datetime

import os
import time
import psycopg2
import psycopg2.extras


class Database:
    """Database SDK"""
    def __init__(self):
        pass
    def select(
            self,
            *,
            query: str,
        ):
        """Select data from the database"""
        result = None
        with psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            ) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                try:
                    cursor.execute(query)
                    result = cursor.fetchall().copy()
                except psycopg2.Error as e:
                    print(e)

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

if __name__ == '__main__':
    pass