import pyspark as ps
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
import logging
import pandas as pd
import numpy as np


class RecipeRecommender():
    """
    Recommendation engine class - uses MLLib Alternating Least Squares Model
    """

    def __init__(self, rank=250, reg=0.1):
        """ Initializes Spark and ALS model selection """
        spark = (
            ps.sql.SparkSession.builder
            .master('local[4]')
            .appName('BVS')
            .getOrCreate()
        )
        self.spark = spark
        self.sc = self.spark.sparkContext

        self.model = ALS(
            maxIter=5,
            rank=rank,
            itemCol='recipe_id',
            userCol='user_id',
            ratingCol='rating',
            nonnegative=True,
            regParam=reg,
#             coldStartStrategy="drop"
            )


    def fit(self, ratings):
        """
        Trains the recommender on a given set of ratings.

        Parameters
        ----------
        ratings : pandas dataframe, shape = (n_ratings, 4)
                  with columns 'user', 'recipe', 'rating'

        Returns
        -------
        self : object
            Returns self.
        """
        """ Convert a Pandas DF to a Spark DF """
        ratings_df = self.spark.createDataFrame(ratings)
        """
        Train the ALS model. We'll call the trained model `recommender`.
        """
        self.recommender_ = self.model.fit(ratings_df)
        return self


    def transform(self, requests):
        """
        Predicts the ratings for a given set of user_id/recipe_id pairs.

        Parameters
        ----------
        requests : pandas dataframe, shape = (n_ratings, 2)
                  with columns 'user', 'movie'

        Returns
        -------
        dataframe : a pandas dataframe with columns 'user', 'movie', 'rating'
                    column 'rating' containing the predicted rating
        """
        # Convert a Pandas DF to a Spark DF
        requests_df = self.spark.createDataFrame(requests)
        self.predictions = self.recommender_.transform(requests_df)
        self.logger.debug("finishing predict")
        return self.predictions.toPandas()


    def evaluate(self, requests, pred_col='prediction'):
        requests_df = self.spark.createDataFrame(requests)
        evaluator = RegressionEvaluator(
                metricName="rmse",
                labelCol="rating",
                predictionCol=pred_col
            )
        rmse = evaluator.evaluate(requests_df)
        return rmse

    def recommend_for_all(self, who='users', number=10):
        if who == 'users':
            user_recs = self.recommender_.recommendForAllUsers(number)
            return (user_recs.toPandas())
        else:
            recipe_recs = self.recommender_.recommendForAllItems(number)
            return (recipe_recs.toPandas)

    def model_save(self, filepath):
        self.recommender_.save(self.sc, filepath)


if __name__ == "__main__":
    pass
