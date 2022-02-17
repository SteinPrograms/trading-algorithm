from pprint import pprint

from database import Database
from settings import Settings


def mean(array : list)->float:
    return sum(array)/len(array)


class Prediction:
    def __init__(self):
        pass

    @staticmethod
    def prediction_with_values_similarity(timeframe: int, resultin: int) -> float:

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
        """The coefficient is the sum from the distance (0 not equal at all and 1 totaly equal) from the actual point and the point of the history

        Raises:
            Exception: When there is not enough data to create the prediction

        Returns:
            _type_: the floating yield 
        """
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
            value = mean(
                dataset[position_of_highest_coefficient + timeframe:position_of_highest_coefficient + timeframe + resultin]
            )/dataset[position_of_highest_coefficient + timeframe]

            return value

        else:
            raise Exception("There is not enough data")
        
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
        """The coefficient is the sum from the distance (0 not equal at all and 1 totaly equal) from the actual perf and the perf between two points of the history

        Raises:
            Exception: When there is not enough data to create the prediction

        Returns:
            _type_: the floating yield 
        """
        for index, value in enumerate(dataset[:-(len(dataframe) + resultin)]):
            dataframe2 = dataset[index: index + len(dataframe)]
            coefficient = sum(
                min(
                    dataframe[index_in_dataframe+1]/dataframe[index_in_dataframe], dataframe2[index_in_dataframe+1]/dataframe2[index_in_dataframe]
                    )
                / max(
                    dataframe[index_in_dataframe+1]/dataframe[index_in_dataframe], dataframe2[index_in_dataframe+1]/dataframe2[index_in_dataframe]
                )
                for index_in_dataframe in range(len(dataframe)-1)
            ) / len(dataframe)

            similarity_coefficients.append(coefficient)

        # Test if there is at least one coefficient
        if similarity_coefficients:
            # Find the position of the closest dataframe
            position_of_highest_coefficient = similarity_coefficients.index(max(similarity_coefficients))
            # Find the performance of what happened after the end of dataframe
            value = mean(
                dataset[position_of_highest_coefficient + timeframe:position_of_highest_coefficient + timeframe + resultin]
            )/dataset[position_of_highest_coefficient + timeframe]

            return value

        else:
            raise Exception("There is not enough data")

    def signal(self):
        predicted_yield = self.prediction_with_pattern_similarity(
            timeframe=Settings().timeframe,
            resultin=Settings().prediction_time
        )

        # If the predicted yield is above the expected yield + fees (since we want to get expected yield (at least))
        if predicted_yield > Settings().real_expected_yield:
            return {
                "signal": "buy", 
                "predicted_yield": predicted_yield,
            }

        else:
            return {
                "signal": "neutral",
                "predicted_yield": predicted_yield,
            }
