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
selected_date = st.slider("Date", min_value=min(df['date']), max_value=max(df['date']), value = datetime.date(2021, 1, 1), format = "YYYY-MMM-DD")
selected_date = str(selected_date)

df_g3 = df.loc[df['date'] == selected_date]
#############


### Slider for selection of data range ###
# replace with st.slider



#############


### Dropdown for National Conditions ###



#############


### Dropdown for Countries ###



#############



### Graph 3: Bar chart across different countries ###




