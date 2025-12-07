import os
import tempfile
from pyspark.sql.functions import col, split
import pandas as pd

from spark_utils import create_spark

spark = create_spark()


def detect_delimiter(content: bytes) -> str:
    """
    Detects whether the file uses comma or semicolon.
    """
    sample = content.decode("utf-8", errors="ignore")
    if sample.count(";") >= sample.count(","):
        return ";"
    return ","


def load_from_uploaded(file):
    """
    Handles uploaded Streamlit file.
    Converts it into a temporary file Spark can read.
    """
    data = file.getvalue()
    sep = detect_delimiter(data)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    tmp.write(data)
    tmp.close()

    return load_spark_dataframe(tmp.name, sep)


def load_from_path(path: str):
    """
    Loads a CSV file from a local path.
    """
    with open(path, "rb") as fh:
        sample = fh.read(2048)
    sep = detect_delimiter(sample)

    return load_spark_dataframe(path, sep)


def load_spark_dataframe(path: str, sep: str):
    """
    Reads the dataset using Spark.
    """
    df = spark.read \
        .option("header", True) \
        .option("sep", sep) \
        .option("encoding", "UTF-8") \
        .option("inferSchema", True) \
        .csv(path)
    return df


def normalize_columns(df):
    """
    Ensures the DataFrame has the correct columns and types.
    Handles cases where the CSV was parsed incorrectly.
    """
    expected = [
        "year", "university", "major", "branch", "language",
        "study_form_symbol", "main_min_score", "main_competition_score",
        "has_subbakalavr", "sub_min_score", "sub_competition_score"
    ]

    if len(df.columns) == 1:
        single = df.columns[0]
        df = df.withColumn("split", split(col(single), ";"))
        for i, name in enumerate(expected):
            df = df.withColumn(name, col("split")[i])
        df = df.drop(single, "split")

    numeric = [
        "main_min_score", "main_competition_score",
        "sub_min_score", "sub_competition_score"
    ]
    for n in numeric:
        if n in df.columns:
            df = df.withColumn(n, col(n).cast("float"))

    return df.filter(col("main_min_score").isNotNull())
