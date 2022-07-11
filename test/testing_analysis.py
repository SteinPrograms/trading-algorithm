import contextlib
from operator import indexOf
from pprint import pprint
from app.logics.settings import Settings
import matplotlib.pyplot as plt
import numpy as np







def filtering(close:list,number_of_passes:int=10,size_of_pass:int=10):
    renta = [(close[index+1]/close[index]-1)*100 for index in range(len(close)-2) ]
    fig, axs = plt.subplots(number_of_passes)

    for num in range(number_of_passes):
        axs[num].plot(list(range(len(renta))),renta)
        index_of_max = indexOf(renta,max(renta,key=abs))
        for i in range(-size_of_pass // 2, size_of_pass // 2+1):
            with contextlib.suppress(Exception):
                renta.remove(renta[index_of_max+i])
        print(np.average(renta))

    plt.show()


filter([row['close'] for row in Settings().broker.get_historical_prices("ETH/USD")])