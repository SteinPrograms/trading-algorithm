#!/usr/bin/env python
"""
Crypto-Currencies trading algorithm using :
    - logics defined in the corresponding package under the prediction.py script
    - docker container hosting the postgres database, python3 instance
"""
__author__ = "Hugo Demenez"

# Common imports
import sys
import time
import os
import threading
from datetime import timedelta,datetime


# Custom imports
from bot_exceptions import DrawdownException
from prediction import Prediction
from position import Position
from database import Database
from routine import Routine
from log import Log
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# create a shared event
event = threading.Event()
# Register the starting date
START_TIME = time.time()

def database_update(database:Database,position:Position):
    """Update server running time to console and database"""
    while not event.is_set():
        # Update the data which gets posted to the database
        if datetime.now().second != 0:
            cleaned = False
        if datetime.now().minute==0 and datetime.now().second == 0 and not cleaned:
            Log("Cleaning logs").clean_logs()
            cleaned = True
        QUERY = f"""
            INSERT INTO vitals
            (id) 
            VALUES(1)
            ON CONFLICT (id) DO UPDATE SET
            running_time = '{str(timedelta(seconds=round(time.time(), 0) - round(START_TIME, 0)))}',
            current_price = '{position.prices.current}',
            status = '{position.settings.status}'
            WHERE vitals.id = 1;
        """
        try:
            database.insert(query = QUERY)
            time.sleep(0.5)
        except Exception as e:
            Log(f"Error {e} while updating database")
            time.sleep(5)

        # If position is opened :
        if position.settings.status == 'open':
            # Update the data which gets posted to the database
            QUERY = f"""
                INSERT INTO positions
                (id)
                VALUES({position.settings.number})
                ON CONFLICT (id) DO UPDATE SET
                
                WHERE positions.id = {position.settings.number};
            """
            try:
                database.insert(query = QUERY)
            except Exception as e:
                Log(f"Error {e} while updating database")

def price_update(position:Position):
    """Update the price of the asset"""
    while not event.is_set():
        position.update_price()
        time.sleep(0.5)

def main():
    """Main loop"""

    Log('PROGRAM START')
    # Starting routines inside a database instance to update program data
    database = Database()

    # Initializing the position
    position = Position()

    predictor = Prediction()

    # Start time updated
    timer_thread = threading.Thread(target=database_update, args=(database,position))
    timer_thread.start()
    api_thread = threading.Thread(target=price_update, args=(position,))
    api_thread.start()

    #Looping into trading program
    while True:
        try:
            if position.settings.status == 'close':
                # Get signal
                if predictor.signal(position.settings.symbol) == 'buy':
                    # Open position
                    position.open_position()
                
            else:
                # Monitoring position
                position.monitor_position()

        # If there is an interrupt
        except (KeyboardInterrupt, DrawdownException):
            event.set()
            Log('PROGRAM END')
            return

if __name__ == '__main__':
    main()
