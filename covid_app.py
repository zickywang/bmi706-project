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

### Title of G3 ###
st.write("# National Conditions and Covid Statistics across Different Countries")
#############

### Filter for COVID Statistics ###
# total deaths per million
stats_options = [
    'new_cases_per_million',
    'total_deaths_per_million',
    'hosp_patients_per_million',
    'icu_patients_per_million'
]
covid_stats = st.selectbox(
    "Covid statistics", options=stats_options)

selected_date = st.slider("Date", min_value=min(df['date']), max_value=max(
    df['date']), value=datetime.date(2021, 1, 1), format="YYYY-MMM-DD")
selected_date = str(selected_date)

df_g3 = df.loc[df['date'] == selected_date]
#############


### Slider for selection of data range ###
# replace with st.slider


#############


### Dropdown for National Conditions ###
default_conditions = [
    'total_vaccinations_per_hundred',
    'stringency_index'
]
condition_options = [
    'gdp_per_capita',  # 'GDP per capita'
    'population_density',
    'extreme_poverty',
    'handwashing_facilities',  # Handwash Facilities
    'total_vaccinations_per_hundred',    # 'Vaccination Rate'
    'stringency_index'
]
conditions = st.multiselect(
    "Select National Conditions", options=condition_options, default=default_conditions)


#############


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
    "Select Countries", options=df["location"].unique(), default=default_countries)

# should be removed later:
# df_g3 = df[df["date"] == '2022-04-26']

df_g3 = df_g3[df_g3["location"].isin(countries)]


#############


### Graph 3: Bar chart across different countries ###
bar_chart = alt.Chart(df_g3).mark_bar().encode(
    x=alt.X("conditions:Q", stack=True, title="conditions"),
    y=alt.Y("location"),
).properties(
    width=440,
    title=f"barchart",
)

st.altair_chart(bar_chart, use_container_width=True)
