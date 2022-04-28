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

selector = alt.selection_single(
    fields=['Age']
)

chart_base = alt.Chart(subset
                       ).properties(
    width=600,
    height=300
).add_selection(
    selector
)


chart_pop = chart_base.mark_bar().encode(
    y=alt.Y("Country"),
    x=alt.X("Pop", title="Population"),
    tooltip=["Pop"],
).properties(
    title=f"Population of {'males' if sex == 'M' else 'females'} in the selected countries in {year} for the selected age group",
).transform_filter(
    selector
)

chart_link = alt.vconcat(chart_rate, chart_pop
                         ).resolve_scale(
    color='independent'
)

st.altair_chart(chart_link, use_container_width=True)
