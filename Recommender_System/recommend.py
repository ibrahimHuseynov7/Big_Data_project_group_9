from pyspark.sql.functions import col, when
import pandas as pd


def recommend(df, year, score, major_filter, include_paid, only_likely, top_n):
    """
    Computes recommendations using Spark filters.
    The final result is returned as a pandas DataFrame for display.
    """
    filtered = df.filter(col("year") == year)

    if not include_paid:
        filtered = filtered.filter((col("study_form_symbol").isNull()) |
                                   (col("study_form_symbol") != "Q"))

    if major_filter:
        filtered = filtered.filter(col("major").contains(major_filter))

    filtered = filtered.filter(col("main_min_score") <= score)

    filtered = filtered.withColumn(
        "prediction",
        when(col("main_competition_score").isNotNull() &
             (col("main_competition_score") <= score), "Likely Admitted")
        .otherwise("Borderline / Competitive")
    )

    if only_likely:
        filtered = filtered.filter(col("prediction") == "Likely Admitted")

    filtered = filtered.orderBy(col("main_min_score").desc())

    return filtered.limit(top_n).toPandas()
