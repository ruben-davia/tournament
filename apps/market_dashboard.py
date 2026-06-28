from __future__ import annotations

import pandas as pd
import streamlit as st

from prediction_framework import build_probability_table


st.set_page_config(page_title="Market Probability Dashboard", layout="wide")
st.title("Market Probability Dashboard")

uploaded = st.file_uploader("Upload options CSV", type=["csv"])
if uploaded is None:
    st.info("Upload a CSV with event_id, option_id, label, and decimal_odds.")
    st.stop()

options = pd.read_csv(uploaded)
probabilities = build_probability_table(options)

st.subheader("Normalized probabilities")
st.dataframe(probabilities, use_container_width=True)

if {"event_id", "label", "truth_probability"}.issubset(probabilities.columns):
    st.bar_chart(probabilities, x="label", y="truth_probability")

