from pprint import pprint

from database import Database
from settings import Settings


class Prediction:
    def __init__(self):
        pass

    @staticmethod
    def prediction_with_pattern_similarity(timeframe: int, resultin: int) -> float:

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

        # Creating the similarity_coefficient for every dataframe
        for index, value in enumerate(dataset[:-(len(dataframe) + resultin)]):
            dataframe2 = dataset[index: index + len(dataframe)]
            coefficient = sum(
                min(dataframe[index_in_dataframe], dataframe2[index_in_dataframe])
                / max(
                    dataframe[index_in_dataframe], dataframe2[index_in_dataframe]
                )
                for index_in_dataframe in range(len(dataframe))
            ) / len(dataframe)

            similarity_coefficients.append(coefficient)

        # Test if there is at least one coefficient
        if similarity_coefficients:
            # Find the position of the closest dataframe
            position_of_highest_coefficient = similarity_coefficients.index(max(similarity_coefficients))
            # Find the performance of what happened after the end of dataframe
            start = dataset[position_of_highest_coefficient + timeframe]
            end = dataset[position_of_highest_coefficient + timeframe + resultin]
            return end / start

        else:
            raise Exception("There is not enough data")

    def buy_signal(self):
        predicted_yield = self.prediction_with_pattern_similarity(
            timeframe=Settings().timeframe_length,
            resultin=Settings().prediction_time
        )

        if predicted_yield > Settings().expected_yield:
            return {"signal": "buy", "yield_for_the_day": predicted_yield}

        else:
            return {"signal": "neutral", "yield_for_the_day": predicted_yield}
