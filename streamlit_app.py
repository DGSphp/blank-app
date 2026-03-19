import streamlit as st

from utils.data_generator import generate_sample_data
from utils.stats import compute_summary_stats, filter_dataframe
from utils.charts import render_line_chart, render_bar_chart, render_scatter_plot

st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")

st.title("📊 Data Explorer")
st.write("An interactive dashboard for exploring and visualizing sample datasets.")


@st.cache_data
def load_data(n_rows: int, seed: int) -> "pd.DataFrame":
    return generate_sample_data(n_rows=n_rows, seed=seed)


# --- Sidebar controls ---
with st.sidebar:
    st.header("Settings")
    n_rows = st.slider("Number of rows", min_value=50, max_value=1000, value=200, step=50)
    seed = st.number_input("Random seed", min_value=0, max_value=9999, value=42)
    selected_categories = st.multiselect(
        "Filter by category",
        options=["A", "B", "C", "D"],
        default=["A", "B", "C", "D"],
    )

df = load_data(n_rows, seed)
filtered_df = filter_dataframe(df, "category", selected_categories)

# --- Summary stats ---
st.header("Summary Statistics")
stats = compute_summary_stats(filtered_df, "value")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Count", stats["count"])
col2.metric("Mean", f"{stats['mean']:.2f}")
col3.metric("Median", f"{stats['median']:.2f}")
col4.metric("Std Dev", f"{stats['std']:.2f}")

# --- Data table ---
with st.expander("View raw data", expanded=False):
    st.dataframe(filtered_df, use_container_width=True)

# --- Charts ---
st.header("Visualizations")
tab_line, tab_bar, tab_scatter = st.tabs(["Trend", "By Category", "Scatter"])

with tab_line:
    render_line_chart(filtered_df)

with tab_bar:
    render_bar_chart(filtered_df)

with tab_scatter:
    render_scatter_plot(filtered_df)
