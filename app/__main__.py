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
from datetime import timedelta

# Custom imports
from bot_exceptions import DrawdownException
from prediction import Prediction
from position import Position
from database import Database
from routine import Routine
from log import Log

# create a shared event
event = threading.Event()
# Register the starting date
START_TIME = time.time()

def database_update(database:Database,position:Position):
    """Update server running time to console and database"""
    while not event.is_set():
        # Update the data which gets posted to the database
        QUERY = f"""INSERT INTO vitals
            (running_time) 
            VALUES('{str(timedelta(seconds=round(time.time(), 0) - round(START_TIME, 0)))}')
            ON CONFLICT (id) DO UPDATE SET
            running_time = '{str(timedelta(seconds=round(time.time(), 0) - round(START_TIME, 0)))}'
            WHERE vitals.id = 1;
        """
        try:
            database.insert(query = QUERY)
        except:
            pass

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

    #Looping into trading program
    while True:
        try:
            position.update_price()
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
            print('\n')
            Log('PROGRAM END')
            return

if __name__ == '__main__':
    main()
