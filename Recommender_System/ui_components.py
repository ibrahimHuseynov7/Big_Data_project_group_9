import plotly.express as px
import streamlit as st


def show_preview(df):
    """
    Displays a preview of the dataset
    """
    with st.expander("Dataset Preview"):
        st.dataframe(df, use_container_width=True)


def show_metrics(result_df):
    """
    Displays high-level summary metrics
    """
    try:
        max_score = float(result_df["main_min_score"].max())
        min_score = float(result_df["main_min_score"].min())
        total = len(result_df)

        c1, c2, c3 = st.columns(3)
        c1.metric("Programs", total)
        c2.metric("Highest minimum score", f"{max_score:.1f}")
        c3.metric("Lowest minimum score", f"{min_score:.1f}")
    except:
        pass


def plot_scores(result_df):
    """
    Plots a bar chart of minimum required scores
    """
    if "main_min_score" not in result_df:
        return

    df = result_df.copy()
    df["label"] = df["university"] + " — " + df["major"]

    fig = px.bar(
        df,
        x="label",
        y="main_min_score",
        labels={"label": "Program", "main_min_score": "Score"},
        height=500
    )

    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    st.subheader("Minimum Score Levels")
    st.plotly_chart(fig, use_container_width=True)
