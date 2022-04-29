from ssl import Options
from turtle import title
import altair as alt
import pandas as pd
import streamlit as st
import datetime

@st.cache
def load_data():
    covid_df = pd.read_csv(
        "https://covid.ourworldindata.org/data/owid-covid-data.csv")
    covid_df['date'] = pd.to_datetime(covid_df['date'])
    return covid_df


# Uncomment the next line when finished
df = load_data()

# Headlines #
st.write("# COVID-19 Data monitor")
st.write("### Source: Our World in Data")

### Radio selector for selection of COVID statistics ###
cov_stats = [
    'New Cases',
    'Hospitalizations',
    'ICU Admissions',
    'Deaths'
]

selected_stat = st.radio("Covid Statistics", options=cov_stats, default = 'New Cases')

cov_map = {
    'New Cases':'new_cases_per_million',
    'Hospitalizations':'hosp_patients_per_million',
    'ICU Admissions':'weekly_icu_admissions_per_million',
    'Deaths':'new_deaths_per_million'
}

### Slider for selection of date range ###
selected_date = st.slider("Date", min_value=min(df['date']), max_value=max(
    df['date']), value=datetime.date(2021, 1, 1), format="YYYY-MMM-DD")
selected_date = str(selected_date)

df = df.loc[df['date'] == selected_date]

### Dropdown for Countries ###
default_countries = [
    'France',
    'United Kingdom',
    'United States',
    'China',
    "Austria",
    "Germany",
    'Taiwan',
    "Iceland",
    "Spain",

]
countries = st.multiselect(
    "Countries", options=df["location"].unique(), default=default_countries)


df = df[df["location"].isin(countries)]

### Plot 1: map ###

### Plot 2: line chart ###

# Plot2 Headline #
st.write("Daily {} per Million People across Countries".format(selected_stat))




### Plot 3: bar chart ###
