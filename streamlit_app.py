from ssl import Options
from turtle import title
import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###
# linzitest


@st.cache
def load_data():
    ## {{ CODE HERE }} ##
    # Move this code into `load_data` function
    covid_df = pd.read_csv(
        "https://covid.ourworldindata.org/data/owid-covid-data.csv")
    # pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
    #     id_vars=["Country", "Year", "Sex"],
    #     var_name="Age",
    #     value_name="Pop",
    # )

    # df = pd.merge(left=cancer_df, right=pop_df, how="left")
    # df["Pop"] = df.groupby(["Country", "Sex", "Age"])[
    #     "Pop"].fillna(method="bfill")
    # df.dropna(inplace=True)

    # df = df.groupby(["Country", "Year", "Cancer",
    #                 "Age", "Sex"]).sum().reset_index()
    # df["Rate"] = df["Deaths"] / df["Pop"] * 100_000

    return df


# Uncomment the next line when finished
df = load_data()

### P1.2 ###


st.write("## Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider
year = st.slider("Year", min_value=min(
    df['Year']), max_value=max(df['Year']), value=2012)
subset = df[df["Year"] == year]
### P2.1 ###


### P2.2 ###
# replace with st.radio
sex = st.radio("Sex", options=("M", "F"))
subset = subset[subset["Sex"] == sex]
### P2.2 ###


### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as `default` for selector)
default_countries = [
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
]

countries = st.multiselect(
    "Countries", options=default_countries, default=default_countries)

subset = subset[subset["Country"].isin(countries)]
### P2.3 ###


### P2.4 ###
# replace with st.selectbox
all_cancer = ['Leukaemia', 'Malignant melanoma of skin',
              'Malignant neoplasm of bladder', 'Malignant neoplasm of breast',
              'Malignant neoplasm of cervix uteri',
              'Malignant neoplasm of colon  rectum and anus',
              'Malignant neoplasm of larynx',
              'Malignant neoplasm of lip oral cavity and pharynx',
              'Malignant neoplasm of liver and intrahepatic bile ducts',
              'Malignant neoplasm of meninges  brain and other parts of central nervous system',
              'Malignant neoplasm of oesophagus',
              'Malignant neoplasm of other and unspecified parts of uterus',
              'Malignant neoplasm of ovary', 'Malignant neoplasm of pancreas',
              'Malignant neoplasm of prostate', 'Malignant neoplasm of stomach',
              'Malignant neoplasm of trachea  bronchus and lung',
              'Multiple myeloma and malignant plasma cell neoplasms',
              "Non-Hodgkin's lymphoma", 'Remainder of malignant neoplasms']

cancer = st.selectbox("Cancer", options=all_cancer)

subset = subset[subset["Cancer"] == cancer]
### P2.4 ###


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

# Original bar chart
# chart = alt.Chart(subset).mark_bar().encode(
#     x=alt.X("Age", sort=ages),
#     y=alt.Y("Rate", title="Mortality rate per 100k"),
#     color="Country",
#     tooltip=["Rate"],
# ).properties(
#     title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
# )

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

rate_scale = alt.Scale(type='log', domain=[0.01, 1000], clamp=True)

chart_rate = chart_base.mark_rect().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Country"),
    color=alt.Color("Rate", scale=rate_scale, title="Mortality rate per 100k"),
    tooltip=["Rate"],
    opacity=alt.condition(selector, alt.value(1), alt.value(0.2))
).properties(
    title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
)

### P2.5 ###

# st.altair_chart(chart_rate, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")


### Bonus ###

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

### Bonus ###
