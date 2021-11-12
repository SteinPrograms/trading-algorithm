from pprint import pprint

from settings import Settings
from database import Database
from datetime import datetime


class Prediction:
    def __init__(self):
        pass

    def predict_yield_for_the_day(self, timeframe: int, resultinXh: int) -> float:

        prices = [{'price': value['price'], 'date': value['date']} for value in
                  Database().database_request("SELECT * FROM price_history ORDER BY date ASC")]

        # Creating dataframe of length timeframe to compare with dataset
        dataframe = [None if index == len(prices) - 1
                     else value['price'] / prices[index + 1]['price']
                     for index, value in enumerate(prices)][-timeframe:][:-1]

        # Creating dataset with the other part of the data
        dataset = [None if index == len(prices) - 1
                   else value['price'] / prices[index + 1]['price']
                   for index, value in enumerate(prices)][:-timeframe][:-1]

        similarity_coefficients = []
        for index, value in enumerate(dataset[:-len(dataframe)]):
            dataframe2 = dataset[index: index + len(dataframe)]
            coefficient = 0
            for index_in_dataframe in range(len(dataframe)):
                coefficient += min(dataframe[index_in_dataframe],
                                   dataframe2[index_in_dataframe])/max(dataframe[index_in_dataframe],
                                                                       dataframe2[index_in_dataframe])
            similarity_coefficients.append(coefficient/len(dataframe))

        pprint(similarity_coefficients)



    def buy_signal(self):
        yield_for_the_day = self.predict_yield_for_the_day()
        if yield_for_the_day > Settings().expected_yield:
            return {"signal": "buy", "yield_for_the_day": yield_for_the_day}

        else:
            return {"signal": "neutral"}
