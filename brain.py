#!/usr/bin/env python

"""
Algorithm which runs when the database is online.
Uses the prediction methode defined in prediction.py to manage a position defined in position.py
"""

from botExceptions import DrawdownException
from position import Position
from settings import Settings
from broker import RealCommands

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
        

    position = Position(backtesting=backtesting)

    
    # Log for server
    print('---Starting Trading---')

    #Looping into trading program
    while True:
        # Clear console
        os.system('cls' if os.name == 'nt' else 'clear')
        # Print program running time in console
        print(f'running_time :{timedelta(seconds=round(time.time(), 0) - round(start_time, 0))}')
        try:
            # If server asks to turnoff the program
            if not Database().launch_program():
                raise ServerStopException
            # If the program total risk is reached
            if position.current_effective_yield < Settings().program_risk:
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

            print("---Ending Trading--")
            return
        
        except ServerStopException :
            # And the position is currently opened
            if position.is_open():
                # Close every position
                position.close_position()
            print("Program paused")
            break



if __name__ == '__main__':
    main()