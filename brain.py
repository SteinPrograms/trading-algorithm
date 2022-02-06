"""Simple program which buys on Monday at 21:00 and Sells on Friday at 21:00"""

import os,threading,time

from datetime import timedelta
from botExceptions import DrawdownException, ServerStopException
from brokerconnection import RealCommands
from database import Database
from position import Position
from settings import Settings

def main():
    """Main method for the brain
    
    Algorithme to manage one position
    """

    # Variables definition
    ## Initializing yields
    total_yield = 1
    highest_yield = 1


    #Looping/awaiting for instructions from database (filled through website)
    while True:
        time.sleep(1)
        #Looking for server instruction
        if Database().launch_program():
            ## Saving start time
            start_time = time.time()
            Database().update_time()
            # Testing connection to broker
            if RealCommands().test_connection():
                print("Connected to market")
                # Not in backtesting mode
                backtesting = False

            elif input("Unable to connect to market, run in back-testing mode? Y/N : ").upper() == 'N':
                return
            else:
                # Entering into backtesting mode
                backtesting = True

            

            # Instantiating the position
            position = Position(backtesting,"BTC")
            
            print(position.backtesting)
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