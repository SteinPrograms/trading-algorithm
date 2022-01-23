"""Simple program which buys on Monday at 21:00 and Sells on Friday at 21:00"""


from datetime import datetime, timedelta
import os
import threading
import time 
from botExceptions import DrawdownException
from brokerconnection import RealCommands
from database import Database
from position import Position
from settings import Settings

def main():
    """Main method for the brain
    
    Function to manage two positions on BTC and ETH simultaneously
    """

    # Variables definition
    ## Initializing yields
    total_yield = 1
    highest_yield = 1


    #Looping/awaiting for instructions from database (filled through website)
    while True:
        
        #Looking for server instruction
        if Database().launch_program():
            ## Saving start time
            start_time = time.time()
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

            list_of_positions = [Position(backtesting,"ETH")]
            print('---Starting Trading---')

            #Looping into trading program
            while True:
                # Clear console
                os.system('cls' if os.name == 'nt' else 'clear')
                # Print program running time in console
                print(f'running_time :{timedelta(seconds=round(time.time(), 0) - round(start_time, 0))}')
                try:
                    
                    positions_yield = sum(
                        position.yield_calculation()
                        for position in list_of_positions
                    )

                    #Refreshing current total yield
                    total_yield +=  (
                        positions_yield - len(list_of_positions)
                    ) / len(list_of_positions)



                    # If the program total risk is reached
                    if highest_yield - total_yield+positions_yield > Settings().program_risk:
                        raise DrawdownException


                    # Managing open positions (checking current yield and if it needs to trigger a sell/buy)
                    for position in list_of_positions:
                        # Starting a thread for every managable position
                        threading.Thread(target=position.manage_position).start()

                    # If server asks to turnoff the program
                    if not Database().launch_program():
                        break


                except KeyboardInterrupt or DrawdownException :
                    # Close every position
                    for position in list_of_positions:
                        if position.is_open():
                            threading.Thread(target=position.close_position).start()

                    print("---Ending Trading--")
                    return


if __name__ == '__main__':
    main()
