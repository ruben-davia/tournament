from __future__ import annotations

import pandas as pd
import streamlit as st

from prediction_framework import build_probability_table, estimate_field_distribution, rank_strategies
from prediction_framework.diagnostics import add_value_diagnostics


st.set_page_config(page_title="Prediction Strategy Dashboard", layout="wide")
st.title("Prediction Strategy Dashboard")

uploaded = st.file_uploader("Upload options CSV", type=["csv"])
if uploaded is None:
    st.info("Upload a CSV with event_id, option_id, label, decimal_odds, popularity_hint, points_if_hit.")
    st.stop()

options = pd.read_csv(uploaded)
n_sims = st.sidebar.number_input("Simulations", min_value=100, max_value=20000, value=2000, step=100)
n_opponents = st.sidebar.number_input("Opponents", min_value=1, max_value=5000, value=100, step=10)
seed = st.sidebar.number_input("Seed", min_value=0, max_value=999999, value=42, step=1)

probabilities = build_probability_table(options)
field = estimate_field_distribution(probabilities)
diagnostics = add_value_diagnostics(field)
summary = rank_strategies(diagnostics, n_sims=int(n_sims), n_opponents=int(n_opponents), seed=int(seed))

st.subheader("Ranked strategies")
st.dataframe(summary, use_container_width=True)

st.subheader("Options with diagnostics")
st.dataframe(diagnostics, use_container_width=True)

