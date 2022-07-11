#!/usr/bin/env python
"""
Crypto-Currencies trading algorithm using :
    - logics defined in the corresponding package under the prediction.py script
    - docker container hosting the postgres database, python3 instance, and the web interface for monitoring purposes
"""

import logging,os,time,settings
from botExceptions import DrawdownException
from position import Position
from brokerconnection import RealCommands
from database import Database
from datetime import timedelta
from routine import Routine

__author__ = "Hugo Demenez"

@Routine(3600)
def testing_connection():
    if not RealCommands().test_connection():
        logging.error("Connection failed")
        exit()

def main():
    # Entering into backtesting mode by default
    BACKTESTING = True

    # Checking broker connectivity
    if RealCommands().test_connection():
        logging.info("MARKET CONNECTION COMPLETE")
        # Starting connectivity check routine
        testing_connection()
        # Not in backtesting mode
        BACKTESTING = False

    elif input("Unable to connect to market, run in back-testing mode? Y/N : ").upper() == 'N':
        return
        
    # Starting routines inside a database instance to update program data
    database = Database()

    # Register the starting date
    START_TIME = time.time()

    # Initializing the position 
    position = Position(backtesting=BACKTESTING,symbol='ETH',database=database)

    # Recover the previous yield to update the total yield
    position.total_yield = 1+float(database.get_server_data()['total_yield'].replace('%','').replace(' ',''))/100
    
    # Logs
    logging.info(f'STARTED AT : {START_TIME}')

    #Looping into trading program
    while True:
        # Must put everything under try block to correctly handle the exception
        try:
            # Clear console
            os.system('cls' if os.name == 'nt' else 'clear')
            # Print program running time in console
            timer = {'running_time':str(timedelta(seconds=round(time.time(), 0) - round(START_TIME, 0)))}
            for data, value__ in timer.items():
                print(data, ':', value__, '\n')

            # Update the data which gets posted to the database
            database.update_data(timer)
            
            # Risky zone
            if position.current_effective_yield < settings.RISK or position.total_yield < settings.DRAWDOWN:
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
            logging.info(f'ENDED AT : {time.time()}')
            return

if __name__ == '__main__':
    logging.basicConfig(filename='output.log', encoding='utf-8', level=logging.DEBUG)
    main()