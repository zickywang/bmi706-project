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

    # impute NA values
    covid_df.iloc[:, 4:] = covid_df.groupby(
        ['location']).fillna(method="ffill").iloc[:, 3:]
    covid_df = covid_df.fillna(0)

    return covid_df


# Uncomment the next line when finished
df = load_data()

### Radio selector for selection of COVID statistics ###
cov_stats = [
    'New Cases',
    'Hospitalizations',
    'ICU Admissions',
    'Deaths'
]

selected_stat = st.radio("Covid Statistics", options=cov_stats)
#############

### Title of G3 ###
st.write("# National Conditions and Covid Statistics across Different Countries")
#############

# ### Filter for COVID Statistics ###
# # total deaths per million
# stats_options = [
#     'new_cases_per_million',
#     'total_deaths_per_million',
#     'hosp_patients_per_million',
#     'icu_patients_per_million'
# ]
# covid_stats = st.selectbox(
#     "Covid statistics", options=stats_options)
# #############


### Slider for selection of data range ###
selected_date = st.slider("Select a date for culmulative statistics since 2020-01-01", min_value=min(df['date']), max_value=max(
    df['date']), value=datetime.date(2021, 1, 1), format="YYYY-MMM-DD")
selected_date = str(selected_date)

df_g3 = df.loc[df['date'] == selected_date]
#############


### Dropdown for National Conditions ###
default_conditions = [
    'gdp_per_capita',
    'people_vaccinated_per_hundred',
    'stringency_index'
]
condition_options = [
    'gdp_per_capita',
    'extreme_poverty',
    'people_vaccinated_per_hundred',
    'people_fully_vaccinated_per_hundred',
    'stringency_index',
    'population_density',
    'median_age',
    'aged_65_older',
    'aged_70_older',
    'cardiovasc_death_rate',
    'diabetes_prevalence',
    'female_smokers',
    'male_smokers',
    'handwashing_facilities',
    'hospital_beds_per_thousand',
    'life_expectancy',
    'human_development_index',
]
conditions = st.multiselect(
    "Select National Conditions", options=condition_options, default=default_conditions)

#############


### Dropdown for Countries ###
option_countries = [
    'Israel',
    'Italy',
    'France',
    'United Kingdom',
    'United States',
    'China',
    'Japan',
    'South Korea',
    "Austria",
    "Germany",
    "Spain",
    'Australia',
    'Central African Republic',
    'Burundi',
    'Liberia',
    'Democratic Republic of Congo',
    'Niger',
    'Malawi',
    'Mozambique',
    'Sierra Leone',
    'Comosros',
    'Madagascar',
    'Togo',
    'Yemen',
    'Yemen',
    'Eritrea',
    'Guinea-Bissau'
]
default_countries = [
    'Israel',
    'Italy',
    'France',
    'United Kingdom',
    'United States',
    'China',
]
covid_countries = df["location"].unique()
countries = st.multiselect(
    "Select Countries", options=option_countries, default=default_countries)

# should be removed later:
# df_g3 = df[df["date"] == '2022-04-26']

df_g3 = df_g3[df_g3["location"].isin(countries)]

#############


### Graph 3: Bar chart across different countries ###
# Header for G3
st.write("#### National Conditions and Culmulative {} per Million People across Countries from 2020-01-01 to {}".format(selected_stat, selected_date))

g3_columns = conditions.copy()
if selected_stat == "New Cases":
    g3_columns.append('total_cases_per_million')
elif selected_stat == "Hospitalizations":
    g3_columns.append('hosp_patients_per_million')
elif selected_stat == "ICU Admissions":
    g3_columns.append('icu_patients_per_million')
else:
    g3_columns.append('total_deaths_per_million')

# wide to long
df_g3_long = pd.melt(df_g3, id_vars=['location', 'date'], value_vars=g3_columns, var_name = 'conditions', value_name='values')

bar_chart = alt.Chart(df_g3_long).mark_bar().encode(
    x=alt.X('values:Q', title="Normalized Values"),
    y=alt.Y("conditions:N", title = None),
    color=alt.Color('conditions:N', title = "National Conditions & {}".format(selected_stat)),
    row=alt.Row('location:N', title = "Country"),
    tooltip = ["values"]
).properties(
    width=440,
)

st.altair_chart(bar_chart, use_container_width=True)
