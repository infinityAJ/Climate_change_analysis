import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache
def load_data():
    return pd.read_csv('data/GlobalTemperatures.csv', parse_dates=['dt'])

df = load_data()
yrwise = df.copy()
yrwise['date'] = pd.to_datetime(yrwise.dt)
yrwise['month'] = yrwise.date.dt.month_name() + yrwise.date.dt.year.agg(lambda x:' '+str(x))
yrwise['year'] = yrwise.date.dt.year
yrwise['century'] = yrwise.year.agg(lambda x:str((x//100)+1)+'th')

def home(title):
    st.title("Introduction")

def page1(title):
    st.title(title)
    if st.sidebar.checkbox("show raw data?"):
        x = st.sidebar.slider('Choose rows to display..', min_value=0,max_value=df.shape[0],value=10)
        st.write(df.head(x))
    st.header("Summary of Dataset")
    st.write(df.describe())
    st.markdown("<hr>", unsafe_allow_html=True)
    cols = st.beta_columns(2)
    cols[0].subheader("Rows of Dataset")
    cols[0].write(df.shape[0])
    cols[1].subheader("Columns of Dataset")
    cols[1].write(df.shape[1])
    st.markdown("<hr>", unsafe_allow_html=True)
    for i in df.columns:
        st.subheader(i)
        divs = st.beta_columns(2)
        divs[0].write(f"Data Type: {type(df[i].iloc[0])}")
        divs[1].write(f"Null Values: {sum(df[i].isna())}")
        st.markdown("<hr>", unsafe_allow_html=True)

def page2(title):
    data = yrwise.copy()
    data = data.groupby('year', as_index=False).agg({
    'LandAverageTemperature': np.mean,
    'LandMaxTemperature':max,
    'LandMinTemperature':min,
    'LandAndOceanAverageTemperature':np.mean}).reset_index()
    st.title(title)
    st.header("Average Temperature of Land throughout the years")
    st.plotly_chart(px.line(data, 'year', 'LandAverageTemperature'))
    data = data.dropna()
    st.header("Maximum Temperature of Land throughout the years")
    st.plotly_chart(px.line(data, 'year', 'LandMaxTemperature'))
    st.header("Minimum Temperature of Land throughout the years")
    st.plotly_chart(px.line(data, 'year', 'LandMinTemperature'))
    st.header("Average Temperature of Land and Ocean throughout the years")
    st.plotly_chart(px.line(data, 'year', 'LandAndOceanAverageTemperature'))

def page3(title):
    data = yrwise.copy()
    data = data.groupby('century', as_index=False).agg({
    'LandAverageTemperature': np.mean,
    'LandMaxTemperature':max,
    'LandMinTemperature':min,
    'LandAndOceanAverageTemperature':np.mean}).reset_index()
    st.title(title)
    st.header("Average Temperature of Land throughout the Centuries")
    st.plotly_chart(px.bar(data, 'century', 'LandAverageTemperature'))
    data = data.dropna()
    st.header("Maximum Temperature of Land throughout the Centuries")
    st.plotly_chart(px.bar(data, 'century', 'LandMaxTemperature'))
    st.header("Minimum Temperature of Land throughout the Centuries")
    st.plotly_chart(px.bar(data, 'century', 'LandMinTemperature'))
    st.header("Average Temperature of Land and Ocean throughout the Centuries")
    st.plotly_chart(px.bar(data, 'century', 'LandAndOceanAverageTemperature'))

def page4(title):
    st.title(title)
    data = yrwise.copy()
    data = data.dropna()
    st.subheader("Hottest Day in Recorded Data")
    st.write(data[data.LandMaxTemperature == max(data.LandMaxTemperature)].date.iloc[0])
    st.subheader("Coldest Day in Recorded Data")
    st.write(data[data.LandMinTemperature == min(data.LandMinTemperature)].date.iloc[0])
    month_data = data.groupby('month', as_index=False).agg({'LandMaxTemperature':max,'LandMinTemperature':min})
    st.subheader("Hottest Month in Recorded Data")
    st.write(month_data[month_data.LandMaxTemperature == max(month_data.LandMaxTemperature)].month.iloc[0])
    st.subheader("Coldest Month in Recorded Data")
    st.write(month_data[month_data.LandMinTemperature == min(month_data.LandMinTemperature)].month.iloc[0])
    year_data = data.groupby('year', as_index=False).agg({'LandMaxTemperature':max,'LandMinTemperature':min})
    st.subheader("Hottest Year in Recorded Data")
    st.write(year_data[year_data.LandMaxTemperature == max(year_data.LandMaxTemperature)].year.iloc[0])
    st.subheader("Coldest Year in Recorded Data")
    st.write(year_data[year_data.LandMinTemperature == min(year_data.LandMinTemperature)].year.iloc[0])
    st.subheader("Hottest Century in Recorded Data")
    century_data = data.groupby('century', as_index=False).agg({'LandMaxTemperature':max,'LandMinTemperature':min})
    st.write(century_data[century_data.LandMaxTemperature == max(century_data.LandMaxTemperature)].century.iloc[0])
    st.subheader("Coldest Century in Recorded Data")
    st.write(century_data[century_data.LandMinTemperature == min(century_data.LandMinTemperature)].century.iloc[0])

pages = {
    "Introduction": home,
    "Information About Data": page1,
    "Climate Changes by Years": page2,
    "Climate Changes by Centuries": page3,
    "General Observations": page4
    }

page = st.sidebar.selectbox('Choose a page...',list(pages.keys()))
pages[page](page)
