


from datetime import datetime, timedelta
import os
import threading
import time 
from botExceptions import DrawdownException
from brokerconnection import RealCommands
from position import Position
from prediction import 

def main():
    """Brain"""
    
    # Testing connection to broker
    
    print("Connected to market")

    


    print('---Starting Trading---')
    # Saving start time
    start_time = time.time()
    list_of_positions = []
    while True:
        # Clear console
        os.system('cls' if os.name == 'nt' else 'clear')
        # Print program running time in console
        print(f'running_time :{timedelta(seconds=round(time.time(), 0) - round(start_time, 0))}')
        try:
            if pred().
            list_of_positions.append(position)
            # If the program total risk is reached
            if 0 - 1 > 0:
                raise DrawdownException


            # Managing open positions (checking current yield and if it needs to trigger a sell/buy)
            for position in list_of_positions:
                # Starting a thread for every managable position
                threading.Thread(target=print,args=(str(position))).start()

        except KeyboardInterrupt or DrawdownException :
            # Managing open positions (checking current yield and if it needs to trigger a sell/buy)
            for position in list_of_positions:
                if position.is_open():
                    threading.Thread(target=position.close_position).start()

            print("---Ending Trading--")
            break
        
        time.sleep(1)


if __name__ == '__main__':
    main()
