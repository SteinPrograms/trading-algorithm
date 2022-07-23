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
import threading
import signal
from datetime import timedelta

# Custom imports
import logging
import settings

from bot_exceptions import DrawdownException
from position import Position
from brokerconnection import RealCommands
from database import Database
from routine import Routine
from logs import logger


def docker_container_terminating():
    """Defining exception raised on keyboard interrupt"""
    raise KeyboardInterrupt()

signal.signal(signal.SIGTERM, docker_container_terminating)


# Register the starting date
START_TIME = time.time()

@Routine(3600)
def testing_connection():
    """Routine testing the broker connection every hour

    return: Exits the python run if the connection fails
    """
    if not RealCommands().test_connection():
        logging.error("Connection failed")
        sys.exit()

# create a shared event
event = threading.Event()


def time_updater(database:Database,position:Position):
    """Update server running time to console and database"""
    while not event.is_set():
        # Print program running time in console
        timer = {
            'running_time':str(timedelta(seconds=round(time.time(), 0) - round(START_TIME, 0)))
        }
        # for data, value__ in timer.items():
        #     output += f"{data} : {value__} | "

        # for data, value__ in position.statistics.items():
        #     output+=f"{data} : {value__} | "

        # print(output,end='\r')

        # Update the data which gets posted to the database
        database.update_server_data(timer)
        database.update_server_data(position.statistics)



def main():
    """Main loop"""

    # Entering into backtesting mode by default
    backtesting = True

    # Checking broker connectivity
    if RealCommands().test_connection():
        logging.info("MARKET CONNECTION COMPLETE")
        # Starting connectivity check routine
        testing_connection()
        # Not in backtesting mode
        backtesting = False

    # Starting routines inside a database instance to update program data
    database = Database()

    # Initializing the position
    position = Position(backtesting=backtesting,symbol='SOL',database=database)

    # Recover the previous yield to update the total yield
    position.total_yield=1
    if database.get_server_data():
        total_yield = database.get_server_data()[0].get('total_yield')
        if total_yield is not None:
            position.total_yield = float(total_yield)

    # Logs
    logger.info('PROGRAM START')

    # Start time updated
    timer_thread = threading.Thread(target=time_updater, args=(database,position))
    timer_thread.start()

    # Start position indicator
    timer_thread = threading.Thread(target=position.market_memory, args=())
    timer_thread.start()

    #Looping into trading program
    while True:
        # Must put everything under try block to correctly handle the exception
        try:
            # Risky zone
            if (position.current_effective_yield < settings.RISK or
                position.total_yield < settings.DRAWDOWN):
                raise DrawdownException

            # Manage position
            position.manage_position()

        # If there is an interrupt
        except (KeyboardInterrupt, DrawdownException):
            event.set()
            # And the position is currently opened
            if position.is_open():
                # Close every position
                position.force_position_close()
                logging.warning('POSITION CLOSED : EXIT')
            logger.info('PROGRAM END')
            return

if __name__ == '__main__':
    logger.info("Starting trading algorithm")
    main()
