import streamlit as st
import os

from config import DEFAULT_CSV_PATH, PAGE_TITLE, LAYOUT, SIDEBAR_STATE, TOP_N
from data_loader import (
    load_from_uploaded,
    load_from_path,
    normalize_columns
)
from recommend import recommend
from ui_components import show_preview, show_metrics, plot_scores


st.set_page_config(
    page_title=PAGE_TITLE,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

st.title("Admission Recommender System")

st.markdown(
    """
This tool helps you explore academic programs that match your test score
and academic interests. The system processes data using Apache Spark.
"""
)


col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Load Dataset")
    uploaded = st.file_uploader("Upload CSV file", type=["csv"])
    path_input = st.text_input("Or enter a file path", value=DEFAULT_CSV_PATH)

with col_right:
    st.subheader("Dataset Guidelines")
    st.info(
        "The CSV file should be semicolon-separated and UTF-8 encoded. "
        "Required columns are detected automatically."
    )

df_spark = None
error_message = None

if uploaded:
    try:
        df_spark = load_from_uploaded(uploaded)
    except Exception as e:
        error_message = str(e)
else:
    if os.path.exists(path_input):
        try:
            df_spark = load_from_path(path_input)
        except Exception as e:
            error_message = str(e)
    else:
        error_message = "The specified file path does not exist."

if error_message:
    st.error(error_message)
    st.stop()

df_spark = normalize_columns(df_spark)
st.success("Dataset loaded successfully.")


try:
    preview = df_spark.limit(8).toPandas()
    show_preview(preview)
except:
    st.warning("Unable to generate preview.")

st.sidebar.header("Filters")

year_values = [r[0] for r in df_spark.select("year").distinct().orderBy("year").collect()]
selected_year = st.sidebar.selectbox("Year", year_values)

major_values = [r[0] for r in df_spark.select("major").distinct().orderBy("major").collect()]
use_dropdown = st.sidebar.checkbox("Select major from list", value=True)

if use_dropdown:
    m = st.sidebar.selectbox("Major", ["(Any)"] + major_values)
    major_filter = None if m == "(Any)" else m
else:
    major_filter = st.sidebar.text_input("Type part of the major", "")

st.sidebar.subheader("Your Score")
sc_s = st.sidebar.slider("Score", min_value=0.0, max_value=700.0, value=400.0, step=0.1)
sc_n = st.sidebar.number_input("Or type score", min_value=0.0, max_value=2000.0, value=sc_s, step=0.1)
score = float(sc_n)

include_paid = st.sidebar.checkbox("Include paid programs", True)
only_likely = st.sidebar.checkbox("Show only likely admitted", False)

start = st.sidebar.button("Find Recommendations")


if start:
    with st.spinner("Processing your request..."):
        result = recommend(
            df_spark,
            selected_year,
            score,
            major_filter,
            include_paid,
            only_likely,
            TOP_N
        )

    if result.empty:
        st.warning("No matching programs found. Try adjusting the filters.")
    else:
        st.success(f"Found {len(result)} suitable programs.")
        st.dataframe(result, use_container_width=True)
        show_metrics(result)
        plot_scores(result)

        with st.expander("Prediction Meaning"):
            st.markdown(
                """
                Likely Admitted: Score meets or exceeds the competition score.  
                Borderline / Competitive: Score is above the minimum but below the competition score.
                """
            )

