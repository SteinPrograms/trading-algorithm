#!/usr/bin/env python

"""
Algorithm which runs when the database is online.
Uses the prediction methode defined in prediction.py to manage a position defined in position.py
"""

from botExceptions import DrawdownException
from position import Position
from settings import Settings
from brokerconnection import RealCommands
from database import Database
import os,time
from datetime import timedelta
__author__ = "Hugo Demenez"

def main():
    
    
    if RealCommands().test_connection():
        print("Connected to market")
        # Not in backtesting mode
        backtesting = False

    elif input("Unable to connect to market, run in back-testing mode? Y/N : ").upper() == 'N':
        return
    else:
        # Entering into backtesting mode
        backtesting = True
        
    start_time = time.time()
    position = Position(backtesting=backtesting)
    position.total_yield = 1+float(Database().get_server_data()['total_yield'].replace('%','').replace(' ',''))/100
    
    # Log for server
    print('---Starting Trading---')

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
            Database().publish_server_data(timer)
            
            
            # If the program total risk is reached
            if position.current_effective_yield < Settings().risk:
                raise DrawdownException

            if position.total_yield < Settings().drawdown:
                raise DrawdownException

            # Manage position
            position.manage_position()
            time.sleep(0.2)

        # If there is an interrupt 
        except KeyboardInterrupt or DrawdownException :                    
            # And the position is currently opened
            if position.is_open():
                # Close every position
                position.force_position_close()
                print("POSITION CLOSED")
            print("---Ending Trading--")
            return
        



if __name__ == '__main__':
    main()