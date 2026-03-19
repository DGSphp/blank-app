import pandas as pd
import streamlit as st


def render_line_chart(df: pd.DataFrame) -> None:
    """Render a line chart of daily average value."""
    if df.empty:
        st.info("No data to display. Adjust filters in the sidebar.")
        return
    daily = df.groupby("date")["value"].mean().reset_index()
    st.line_chart(daily, x="date", y="value")


def render_bar_chart(df: pd.DataFrame) -> None:
    """Render a bar chart of mean value per category."""
    if df.empty:
        st.info("No data to display. Adjust filters in the sidebar.")
        return
    by_cat = df.groupby("category")["value"].mean().reset_index()
    st.bar_chart(by_cat, x="category", y="value")


def render_scatter_plot(df: pd.DataFrame) -> None:
    """Render a scatter plot of value vs score."""
    if df.empty:
        st.info("No data to display. Adjust filters in the sidebar.")
        return
    st.scatter_chart(df, x="value", y="score", color="category")
