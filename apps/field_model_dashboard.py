from __future__ import annotations

import pandas as pd
import streamlit as st

from prediction_framework import build_probability_table, estimate_field_distribution
from prediction_framework.diagnostics import add_value_diagnostics


st.set_page_config(page_title="Field Model Dashboard", layout="wide")
st.title("Field Model Dashboard")

uploaded = st.file_uploader("Upload options CSV", type=["csv"])
if uploaded is None:
    st.info("Upload a CSV with event_id, option_id, label, decimal_odds, and optional popularity_hint.")
    st.stop()

chalk_weight = st.sidebar.slider("Truth/chalk weight", 0.1, 3.0, 1.0, 0.1)
popularity_weight = st.sidebar.slider("Popularity weight", 0.0, 3.0, 1.0, 0.1)

options = pd.read_csv(uploaded)
probabilities = build_probability_table(options)
field = estimate_field_distribution(
    probabilities,
    chalk_weight=float(chalk_weight),
    popularity_weight=float(popularity_weight),
)
diagnostics = add_value_diagnostics(field)

st.subheader("Field probabilities")
st.dataframe(diagnostics, use_container_width=True)

if {"label", "truth_probability", "field_probability"}.issubset(diagnostics.columns):
    chart_data = diagnostics[["label", "truth_probability", "field_probability"]].set_index("label")
    st.bar_chart(chart_data)

