from ssl import Options
from turtle import title
import altair as alt
import pandas as pd
import streamlit as st


@st.cache
def load_data():
    covid_df = pd.read_csv(
        "https://covid.ourworldindata.org/data/owid-covid-data.csv")
    return covid_df


# Uncomment the next line when finished
df = load_data()

# Headlines #
st.write("# COVID-19 Data monitor")
st.write("### Source: Our World in Data")

### Plot 1 ###

### Plot 2 ###

### Plot 3: bar chart ###
