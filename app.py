import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Global Temperature Dashboard",
    page_icon="🌍",
    layout="wide"
)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Steven-Alvarado/Global-Temperature-Analysis/refs/heads/main/GlobalTemperatures.csv"
    df = pd.read_csv(url)
    df['dt'] = pd.to_datetime(df['dt'])
    df['Year'] = df['dt'].dt.year
    df.dropna(subset=['LandAverageTemperature'], inplace=True)
    return df

df = load_data()
st.title("Global Temperature Trends Dashboard")
st.markdown("Explore how average land temperatures have changed over time.")
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Select Year Range",
                              int(df['Year'].min()),
                              int(df['Year'].max()),
                              (1900,2015)
                              )
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
st.write(f"## Temperature Trend from {year_range[0]} to {year_range[1]}")
yearly_temp = filtered_df.groupby('Year')['LandAverageTemperature'].mean().reset_index()
st.write("### Average Temperature Trend")
fig_line = px.line(
    yearly_temp,
    x='Year',
    y='LandAverageTemperature',
    title='Global Average Land Temperature Over Time',
    labels={'Year': 'Year', 'LandAverageTemperature': 'Average Temperature (°C)'}
)
fig_line.update_traces(mode='lines+markers')
fig_line.add_scatter(x=yearly_temp['Year'], y=yearly_temp['LandAverageTemperature'].rolling(window=10).mean(), mode='lines', name='10-Year Moving Average')
st.plotly_chart(fig_line, use_container_width=True)
st.write("### Raw Data")
with st.expander("Show Filtered Data"):
    st.dataframe(filtered_df)
