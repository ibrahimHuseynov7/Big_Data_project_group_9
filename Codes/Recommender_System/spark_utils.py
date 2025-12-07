import os
import sys
from pyspark.sql import SparkSession

# Ensure PySpark uses the correct Python interpreter
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable


def create_spark():
    """
    Creates and returns a SparkSession.
    This is called once and reused by the application.
    """
    spark = SparkSession.builder \
        .appName("Admission-Recommender") \
        .config("spark.ui.showConsoleProgress", "false") \
        .getOrCreate()
    return spark
