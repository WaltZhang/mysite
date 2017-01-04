from django.db import models
from django.contrib.auth.models import User
from .sparks import Spark


class Project(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.name


class Dataset(models.Model):
    user = models.ForeignKey(User, default=1)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    creator = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.name


class AQI(object):
    def __init__(self):
        self._sc = Spark()

    def save_aqi(self):
        dataset_cols = ['name', 'creator', 'created_time', 'attributes']
        datasets = [('AQI', 'walt', '2017-01-03', ['id', 'location', 'date', 'aqi']), ]
        rdd = self._sc.spark.sparkContext.parallelize(datasets)
        df = self._sc.spark.createDataFrame(rdd, dataset_cols)
        # list = [{'name': 'Alice', 'id': 1}, {'name': 'Bob', 'id': 2}, {'name': 'Peter', 'id': 3}]
        # df = self._sc.spark.createDataFrame(list)
        df.write.saveAsTable('AQI')

    def load_aqi(self, query=None):
        string = 'SELECT * FROM AQI'
        if query is not None:
            string += ' ' + query
        df = self._sc.spark.sql(string)
        return df
