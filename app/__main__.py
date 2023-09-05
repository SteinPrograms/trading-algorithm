#!/usr/bin/env python
"""
Crypto-Currencies trading algorithm using :
    - logics defined in the corresponding package under the prediction.py script
    - docker container hosting the postgres database, trading instance and postgres api
"""
__author__ = "Hugo Demenez"

import logging
import os
# Common imports
import sys
import threading
import time
from datetime import datetime, timedelta

# Custom imports
from bot_exceptions import DrawdownException
from dotenv import load_dotenv
from indicator import Indicator
from position import Position
from helpers import database

# Load environment variables
load_dotenv()
# create a shared event
event = threading.Event()
# Register the starting date
START_TIME = time.time()

def database_update(position:Position):
    """
    Update vitals and position data to database
    """
    while not event.is_set():
        # Update the data which gets posted to the database
        QUERY = f"""
            INSERT INTO positions
            (id)
            VALUES({position.settings.id})
            ON CONFLICT (id) DO UPDATE SET
            open_price = {position.prices.open},
            close_price = {position.prices.close},
            highest_price = {position.prices.highest},
            lowest_price = {position.prices.lowest},
            current_price = {position.prices.current},
            open_date = '{position.times.open}',
            close_date = '{position.times.close}',
            status = '{position.settings.status}',
            exit_mode = '{position.settings.exit_mode}'
            WHERE positions.id = {position.settings.id};
        """
        try:
            database.insert(query = QUERY)
        except Exception as e:
            logging.warning(f"Error {e} while updating positions in database")

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
            logging.warning(f"Error {e} while updating vitals in database")
            time.sleep(5)

        

def market_update(position:Position, indicator : Indicator):
    """Update the price of the asset"""
    while not event.is_set():
        indicator.get_signal(position.settings.symbol)
        position.prices.current = indicator.close
        time.sleep(0.3)

def main():
    """Main loop"""

    logging.info('PROGRAM START')

    # Initialize instances
    indicator = Indicator()
    position = Position()

    # Start threads
    timer_thread = threading.Thread(target=database_update, args=(position,))
    timer_thread.start()
    broker_interaction_thread = threading.Thread(target=market_update, args=(position,indicator))
    broker_interaction_thread.start()

    while True:
        try:
            if position.settings.status == 'close':
                # Get signal
                if indicator.signal == 'buy':
                    # Open position
                    position.open_position()
                
            else:
                # Monitoring position
                position.monitor_position(indicator=indicator)

        # If there is an interrupt
        except (KeyboardInterrupt, DrawdownException):
            event.set()
            logging.info('PROGRAM END')
            return

if __name__ == '__main__':
    main()
