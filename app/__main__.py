#!/usr/bin/env python
"""
Crypto-Currencies trading algorithm using :
    - logics defined in the corresponding package under the prediction.py script
    - docker container hosting the postgres database, python3 instance
"""
__author__ = "Hugo Demenez"

# Common imports
import os
import sys
import time

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

    elif input("Unable to connect to market, run in back-testing mode? Y/N : ").upper() == 'N':
        return

    # Starting routines inside a database instance to update program data
    database = Database()


    # Initializing the position 
    position = Position(backtesting=backtesting,symbol='ETH',database=database)

    # Recover the previous yield to update the total yield
    position.total_yield = 1+float(database.get_server_data().get('total_yield',0).
        replace('%','').
        replace(' ',''))/100

    # Logs
    logger.info('STARTED AT : %s',START_TIME)

    #Looping into trading program
    while True:
        # Must put everything under try block to correctly handle the exception
        try:
            # Clear console
            os.system('cls' if os.name == 'nt' else 'clear')
            # Print program running time in console
            timer = {
                'running_time':str(timedelta(seconds=round(time.time(), 0) - round(START_TIME, 0)))
            }
            for data, value__ in timer.items():
                print(data, ':', value__, '\n')

            # Update the data which gets posted to the database
            database.update_data(timer)

            # Risky zone
            if (position.current_effective_yield < settings.RISK or
                position.total_yield < settings.DRAWDOWN):
                raise DrawdownException

            # Manage position
            position.manage_position()

        # If there is an interrupt
        except (KeyboardInterrupt, DrawdownException):                    
            # And the position is currently opened
            if position.is_open():
                # Close every position
                position.force_position_close()
                logging.warning('POSITION CLOSED : EXIT')
            logger.info('ENDED AT : %s',time.time())
            return

if __name__ == '__main__':
    logger.info("Starting trading algorithm")
    main()
