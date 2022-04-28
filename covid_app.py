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

### Title of G3 ###
st.write("# National Conditions and Covid Statistics across Different Countries")
#############

### Filter for COVID Statistics ###
# total deaths per million


#############



### Slider for selection of data range ###
# replace with st.slider



#############


### Dropdown for National Conditions ###



#############


### Dropdown for Countries ###



#############



### Graph 3: Bar chart across different countries ###




