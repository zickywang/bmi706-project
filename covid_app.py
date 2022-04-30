from ssl import Options
from turtle import title
import altair as alt
import pandas as pd
import streamlit as st
import datetime
from datetime import time

@st.cache
def load_data():
    covid_df = pd.read_csv(
        "https://covid.ourworldindata.org/data/owid-covid-data.csv")
    covid_df['date'] = pd.to_datetime(covid_df['date']).dt.date
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

selected_stat = st.radio("Covid Statistics", options=cov_stats)

### Slider for selection of date range ###
start_date, end_date = st.slider("Date", min(df['date']), max(df['date']), 
    (datetime.date(2021, 1, 1), max(df['date'])), format="YYYY-MMM-DD")

df = df[(df['date'] > start_date) & (df['date'] < end_date)]
df["date"] = pd.to_datetime(df["date"])

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


# multi-line tooltip
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['date'], empty='none')

selectors = alt.Chart(df).mark_point().encode(
    x='date',
    opacity=alt.value(0),
).add_selection(
    nearest
)

if selected_stat == 'New Cases':
    base = alt.Chart(df
    ).mark_line().encode(
        x='date',
        y='new_cases_smoothed_per_million',
        color='location',
        tooltip = ['new_cases_smoothed_per_million', 'location']
    )
    text = base.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'new_cases_smoothed_per_million', alt.value(' '))
    )
elif selected_stat == 'Hospitalizations':
    base = alt.Chart(df
    ).mark_line().encode(
        x='date',
        y='hosp_patients_per_million',
        color='location',
        tooltip = ['hosp_patients_per_million', 'location']
    )
    text = base.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'hosp_patients_per_million', alt.value(' '))
    )
elif selected_stat == 'ICU Admissions':
    base = alt.Chart(df
    ).mark_line().encode(
        x='date',
        y='weekly_icu_admissions_per_million',
        color='location',
        tooltip = ['weekly_icu_admissions_per_million', 'location']
    )
    text = base.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'weekly_icu_admissions_per_million', alt.value(' '))
    )
else:
    base = alt.Chart(df
    ).mark_line().encode(
        x='date',
        y='new_deaths_smoothed_per_million',
        color='location',
        tooltip = ['new_deaths_smoothed_per_million', 'location']
    )
    text = base.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'new_deaths_smoothed_per_million', alt.value(' '))
    )


points = base.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

rules = alt.Chart(df).mark_rule(color='gray').encode(
    x='date',
).transform_filter(
    nearest
)

g2 = alt.layer(
    base, selectors, points, rules, text
).properties(
    width=800, height=600
)
g2
### Plot 3: bar chart ###
