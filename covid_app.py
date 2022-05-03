# from ssl import Options
# from turtle import title
import altair as alt
import pandas as pd
import streamlit as st
import datetime
import time
import pydeck as pdk

@st.cache
def load_data():
    covid_df = pd.read_csv(
        "https://github.com/zickywang/bmi706-project/blob/main/covid_dataset.csv")

    covid_df['date'] = pd.to_datetime(covid_df['date'])

    # impute NA values
    covid_df.iloc[:, 4:] = covid_df.groupby(
        ['location']).fillna(method="ffill").iloc[:, 3:]
    covid_df = covid_df.fillna(0)

    return covid_df

# Load data and normalize data for G3
df = load_data()
df_norm = df.iloc[:, 4:]/df.iloc[:, 4:].max()
df_norm.columns = [
    str(df_norm) + '_norm' for df_norm in df_norm.columns]
df_norm = pd.concat((df.iloc[:, :4], df_norm), 1)

# Headlines #
st.write("# COVID-19 Data monitor")
st.write("### Source: Our World in Data")

### Radio selector for selection of COVID statistics: G1, G2, G3 ###
st.write("##### Select a COVID statistics for all visualizations below")

cov_stats = [
    'New Cases',
    'Hospitalizations',
    'ICU Admissions',
    'Deaths'
]

selected_stat = st.radio("Covid Statistics", options=cov_stats)
#############

### Plot 1: map ###
### Slider for selection of date range ###
### Slider for selection of date range: G1 and G2 ###
start_date, end_date = st.slider("Select a range of date", min_value=datetime.date(2020, 6, 1), max_value=max(df['date'].dt.date), value=[datetime.date(2021, 4, 1), datetime.date(2022, 1, 1)], format="YYYY-MMM-DD")
start_date = str(start_date)
end_date = str(end_date)
df_g2 = df.loc[(df['date'] > start_date) & (df['date'] < end_date)]

### SELECTBOX widgets
st.write("THE map")

metric = None
if selected_stat == "New Cases":
    metric = 'total_cases_per_million'
elif selected_stat == "Hospitalizations":
    metric = 'hosp_patients_per_million'
elif selected_stat == "ICU Admissions":
    metric = 'icu_patients_per_million'
else:
    metric = 'total_deaths_per_million'

#################################################
## MAP

# Variable for date picker, default to Jan 1st 2021
date = datetime.date(2021,1,1)

# Set viewport for the deckgl map
view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)

# Create the scatter plot layer
covidLayer = pdk.Layer(
        "ScatterplotLayer",
        data=df_g2,
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["Longitude", "Latitude"],
        get_radius=metric,
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

# Update the maps and the subheading each day for from beginning to end
for i in range(0, 100, 1):
    # Increment day by 1
    date += datetime.timedelta(days=1)

    # Update data in map layers
    covidLayer.data = df[df['date'] == date.isoformat()]

    # Update the deck.gl map
    r.update()

    # Render the map
    map.pydeck_chart(r)

    # Update the heading with current date
    ######!!!!!!!! beautify
    subheading.subheader("%s on : %s" % (metric, date.strftime("%B %d, %Y")))
    
    # wait 0.1 second before go onto next day
    time.sleep(0.05)


### Dropdown for Countries: G2 and G3 ###
default_countries = [
    'Japan',
    'United Kingdom',
    'Italy',
    'France',
]
option_countries = df["location"].unique()
countries = st.multiselect(
    "Select Countries", options=option_countries, default=default_countries)
##############


############### G2 ###############
# move to share with g1 and g2
# ### Slider for selection of date range: G2 ###
# start_date, end_date = st.slider("Select a range of date", min_value=datetime.date(2020, 6, 1), max_value=max(df['date']), value=[datetime.date(2021, 4, 1), datetime.date(2022, 1, 1)], format="YYYY-MMM-DD")
# start_date = str(start_date)
# end_date = str(end_date)
# df_g2 = df.loc[(df['date'] > start_date) & (df['date'] < end_date)]
#############

# filter countries
df_g2 = df_g2[df_g2["location"].isin(countries)]

# Plot2 Headline 
st.write("#### Daily {} per Million People across Countries".format(selected_stat))

# multi-line tooltip
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['date'], empty='none')

selectors = alt.Chart(df_g2).mark_point().encode(
    x='date',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# base line plot
if selected_stat == 'New Cases':
    base = alt.Chart(df_g2
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
    base = alt.Chart(df_g2
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
    base = alt.Chart(df_g2
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
    base = alt.Chart(df_g2
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

rules = alt.Chart(df_g2).mark_rule(color='gray').encode(
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
############### G2 ###############


############### G3 ###############
### Graph 3: Bar chart across different countries ###
### Title of G3 ###
st.write("#### National Conditions and Covid Statistics across Different Countries")
#############

### Slider for selection of date for culmulative data ###
selected_date = st.slider("Select a date for culmulative statistics since 2020-01-01", min_value=datetime.date(2020, 6, 1), max_value=max(
    df['date'].dt.date), value=datetime.date(2021, 1, 1), format="YYYY-MMM-DD")
selected_date = str(selected_date)

df_g3 = df.loc[df['date'] == selected_date]
#############

# df_g3_norm = df_g3.iloc[:, 4:]/df_g3.iloc[:, 4:].max()
df_g3_norm = df_norm.loc[df_norm['date'] == selected_date]


### Dropdown for National Conditions ###
default_conditions = [
    'gdp_per_capita',
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
# option_countries = [
#     'Israel',
#     'Italy',
#     'France',
#     'United Kingdom',
#     'United States',
#     'Japan',
#     'South Korea',
#     "Austria",
#     "Germany",
#     "Spain",
#     'Australia',
#     'Central African Republic',
#     'Burundi',
#     'Liberia',
#     'Democratic Republic of Congo',
#     'Niger',
#     'Malawi',
#     'Mozambique',
#     'Sierra Leone',
#     'Comosros',
#     'Madagascar',
#     'Togo',
#     'Yemen',
#     'Eritrea',
#     'Guinea-Bissau'
# ]

# default_countries = [
#     'Japan',
#     'United Kingdom',
#     'Italy',
#     'France',
# ]
# option_countries = df["location"].unique()
# countries = st.multiselect(
#     "Select Countries", options=option_countries, default=default_countries)


df_g3 = df_g3[df_g3["location"].isin(countries)]
df_g3_norm = df_g3_norm[df_g3_norm["location"].isin(countries)]
#############


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

g3_columns_norm = [
    str(i) + '_norm' for i in g3_columns]

# wide to long
df_g3_long = pd.melt(df_g3, id_vars=[
    'location', 'date'], value_vars=g3_columns, var_name='conditions', value_name='values')

df_g3_norm_long = pd.melt(df_g3_norm, id_vars=[
    'location', 'date'], value_vars=g3_columns_norm, var_name='conditions', value_name='values_norm')
df_g3_long = pd.concat((df_g3_long, df_g3_norm_long.iloc[:, -1:]), 1)

bar_chart = alt.Chart(df_g3_long).mark_bar().encode(
    x=alt.X('values_norm:Q', title="Normalized Values"),
    y=alt.Y("conditions:N", title=None, sort=g3_columns),
    color=alt.Color(
        'conditions:N', title="National Conditions & {}".format(selected_stat)),
    row=alt.Row('location:N', title="Country", sort=countries),
    tooltip=["values:Q"]
)
# .properties(
#     width=800
# )

st.altair_chart(bar_chart, use_container_width=True)
############### G3 ###############
