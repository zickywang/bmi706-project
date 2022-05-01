from ssl import Options
from turtle import title
import altair as alt
import pandas as pd
import streamlit as st
import datetime
from datetime import time
import pydeck as pdk

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

#################################################
### Plot 1: map ###

#################################################
### SELECTBOX widgets
metrics =['total_cases_per_million','new_cases_smoothed_per_million','total_deaths_per_million','new_deaths_smoothed_per_million', 
'icu_patients_per_million', 'hosp_patients_per_million', 'weekly_icu_admissions_per_million', 'weekly_hosp_admissions_per_million', 
'total_tests_per_thousand', 'new_tests_smoothed_per_thousand']

cols = st.selectbox('Covid metric to view', metrics)

# let's ask the user which column should be used as Index
if cols in metrics:   
    metric_to_show_in_covid_Layer = cols 

#################################################
## MAP

# Variable for date picker, default to Jan 1st 2020
date = datetime.date(2020,1,1)

# Set viewport for the deckgl map
view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)

# Create the scatter plot layer
covidLayer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["Longitude", "Latitude"],
        get_radius=metric_to_show_in_covid_Layer,
        get_fill_color=[252, 136, 3],
        get_line_color=[255,0,0],
        tooltip="test test",
    )

# Create the deck.gl map
r = pdk.Deck(
    layers=[covidLayer],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/light-v10",
)

# Create a subheading to display current date
subheading = st.subheader("")

# Render the deck.gl map in the Streamlit app as a Pydeck chart 
map = st.pydeck_chart(r)

# Update the maps and the subheading each day for 90 days
for i in range(0, 120, 1):
    # Increment day by 1
    date += datetime.timedelta(days=1)

    # Update data in map layers
    covidLayer.data = df[df['date'] == date.isoformat()]

    # Update the deck.gl map
    r.update()

    # Render the map
    map.pydeck_chart(r)

    # Update the heading with current date
    subheading.subheader("%s on : %s" % (metric_to_show_in_covid_Layer, date.strftime("%B %d, %Y")))
    
    # wait 0.1 second before go onto next day
    time.sleep(0.05)

#################################################
### Plot 2: line chart ###

# Plot2 Headline 
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

# base line plot
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

# wrap them together
g2 = alt.layer(
    base, selectors, points, rules, text
).properties(
    width=800, height=600
)
g2

#################################################
### Plot 3: bar chart ###
