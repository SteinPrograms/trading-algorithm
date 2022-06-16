#!/usr/bin/env python

"""
Algorithm which runs when the database is online.
Uses the prediction methode defined in prediction.py to manage a position defined in position.py
"""

import logging
from exceptions.botExceptions import DrawdownException
from logics.position import Position
from logics.settings import Settings
from broker.brokerconnection import RealCommands
from database.database import Database
import os,time
from datetime import timedelta
from routine import Routine

__author__ = "Hugo Demenez"

@Routine(3600)
def testing_connection():
    if not RealCommands().test_connection():
        logging.error("Connection failed")
        exit()

def main():

    logging.basicConfig(filename='output.log', encoding='utf-8', level=logging.DEBUG)

    if RealCommands().test_connection():
        logging.info("Connected to market")
        testing_connection()
        # Not in backtesting mode
        backtesting = False

    elif input("Unable to connect to market, run in back-testing mode? Y/N : ").upper() == 'N':
        return
    else:
        # Entering into backtesting mode
        backtesting = True
    
    # Starting routines inside a database instance to update program data to mongodb
    database = Database()

    # Register the starting date
    start_time = time.time()

    # Initializing the position 
    position = Position(backtesting=backtesting,symbol='ETH',database=database)

    # Recover the previous yield to update the total yield
    position.total_yield = 1+float(database.get_server_data()['total_yield'].replace('%','').replace(' ',''))/100
    
    # Logs
    logging.info(f'Started program at : {time.time()}')

    

    #Looping into trading program
    while True:
        # Must put everything under try block to correctly handle the exception
        try:
            # Clear console
            os.system('cls' if os.name == 'nt' else 'clear')
            # Print program running time in console
            timer = {'running_time':str(timedelta(seconds=round(time.time(), 0) - round(start_time, 0)))}
            for data, value__ in timer.items():
                print(data, ':', value__, '\n')

            # Update the data which gets posted to the database
            database.update_data(timer)
            
            
            # Risky zone
            if position.current_effective_yield < Settings().risk or position.total_yield < Settings().drawdown:
                raise DrawdownException


            # Manage position
            position.manage_position()

        # If there is an interrupt 
        except KeyboardInterrupt or DrawdownException :                    
            # And the position is currently opened
            if position.is_open():
                # Close every position
                position.force_position_close()
                logging.warning('Position closed : on program exit')
            logging.info(f'Ended program at : {time.time()}')
            return
        



if __name__ == '__main__':
    main()