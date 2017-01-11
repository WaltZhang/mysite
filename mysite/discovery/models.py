from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .sparks import Spark


class Project(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=200)
    created_time = models.DateTimeField('date created')

    def __str__(self):
        return self.name


class Dataset(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=200)
    creator = models.CharField(max_length=200)
    created_time = models.DateTimeField('date created')
    attributes = models.TextField()

    def __str__(self):
        return self.name


class Collection(object):
    def __init__(self, collection_name):
        self._collection = collection_name
        self._sc = Spark()

    def to_spark(self):
        sql = 'SELECT * FROM ' + self._collection
        return self._sc.spark.sql(sql)


class AQI(object):
    def __init__(self):
        self._sc = Spark()

    def save_aqi(self):
        dataset_cols = ['name', 'creator', 'created_time', 'attributes']
        ds = Dataset()
        ds.name = 'aqi'
        ds.creator = 'walt'
        ds.created_time = timezone.now()
        ds.attributes = 'location||date||aqi'
        ds.save()
        # datasets = [('aqi', 'walt', '2017-01-03', 'location||date||aqi'), ]
        # rdd = self._sc.spark.sparkContext.parallelize(datasets)
        # df1 = self._sc.spark.createDataFrame(rdd, dataset_cols)
        # df1 = df1.withColumn('created_time', df1.created_time.cast('timestamp').alias('created_time'))
        # list = [{'name': 'Alice', 'id': 1}, {'name': 'Bob', 'id': 2}, {'name': 'Peter', 'id': 3}]
        # df = self._sc.spark.createDataFrame(list)
        # df1.write.saveAsTable('mdr')
        aqi = [('Shanghai', '2017-01-02', 100),]
        df2 = self._sc.spark.createDataFrame(aqi, ['location', 'date', 'aqi'])
        df2.write.saveAsTable('aqi')

    def load_aqi(self, query=None):
        string = 'SELECT * FROM AQI'
        if query is not None:
            string += ' ' + query
        df = self._sc.spark.sql(string)
        return df