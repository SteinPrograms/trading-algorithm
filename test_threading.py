import threading
import os
from datetime import timedelta
import time


START_TIME=time.time()


def time_updater():
    """Updating time in real time"""
    while True:
        # Clear console
        os.system('cls' if os.name == 'nt' else 'clear')
        # Print program running time in console
        timer = {
            'running_time':str(timedelta(seconds=round(time.time(), 0) - round(START_TIME, 0)))
        }
        for data, value__ in timer.items():
            print(data, ':', value__, '\n')
            print(variable)


if __name__=="__main__":
    variable = 0
    # Start time updated
    timer_thread = threading.Thread(target=time_updater,args=())
    timer_thread.start()
    while True:
        variable += 1
        time.sleep(2)
