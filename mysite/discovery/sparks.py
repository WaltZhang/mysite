import os
import sys
from django.conf import settings
from pyspark.sql.session import SparkSession


class Spark:
    def __init__(self, app_name='django-spark', master='local'):
        spark_home = settings.SPARK_HOME if settings.SPARK_HOME else '/usr/local/spark'
        os.environ['SPARK_HOME'] = spark_home
        sys.path.insert(0, settings.PYTHONPATH if settings.PYTHONPATH else os.path.join(spark_home, 'python'))
        sys.path.insert(0, settings.PYSPARK_DIR if settings.PYSPARK_DIR else os.path.join(spark_home, 'python/pyspark'))
        if settings.PYSPARK_PYTHON:
            os.environ['PYSPARK_PYTHON'] = settings.PYSPARK_PYTHON
        if settings.JAVA_HOME:
            os.environ['JAVA_HOME'] = settings.JAVA_HOME
        if settings.HADOOP_CONF_DIR:
            os.environ['HADOOP_CONF_DIR'] = settings.HADOOP_CONF_DIR
        self.spark = self.init_spark(app_name, master)

    def init_spark(self, app_name, master):
        return SparkSession\
            .builder\
            .appName(app_name)\
            .enableHiveSupport() \
            .master(master)\
            .getOrCreate()
        # .config("spark.sql.warehouse.dir", '/Users/walt/Development/python/mysite')\

