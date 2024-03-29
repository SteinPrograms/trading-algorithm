"""SDK for the postgres database"""

from datetime import datetime
import logging
import os
import time
import psycopg2
import psycopg2.extras

def select(
        *,
        query: str,
        params: tuple = None,
    ):
    """Create a temporary connection to the database, execute a query and return the result"""
    try:
        with psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
        ) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall().copy()
                logging.info(f"SELECT query executed: {query}")
    except Exception as e:
        logging.error(f"SELECT query failed: {query}, error: {e}")
        raise

    return result

def insert(
        *,
        query: str,
        params: tuple = None,
    ):
    """Create a temporary connection to the database and execute a query"""
    try:
        with psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                logging.info(f"INSERT query executed: {query}")
    except Exception as e:
        logging.error(f"INSERT query failed: {query}, error: {e}")
        raise
