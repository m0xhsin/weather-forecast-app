import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from model import predict_temperature
from weather_utils import weather_description

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Germany Weather Dashboard", layout="wide")

st_autorefresh(interval=60000, key="datarefresh")

st.markdown(
    "<h1 style='text-align:center; color:#1f77b4;'>🇩🇪 Germany Weather Intelligence Dashboard</h1>",
    unsafe_allow_html=True
)

cities = requests.get(f"{API_URL}/cities").json()
city = st.selectbox("Search German City", cities)

response = requests.get(f"{API_URL}/weather/{city}")
data = response.json()

st.subheader(f"🌍 Current Weather in {city}")

current = data["current_weather"]

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡 Temperature", f"{current['temperature']} °C")
col2.metric("💨 Wind Speed", f"{current['windspeed']} km/h")
col3.metric("🧭 Wind Direction", f"{current['winddirection']}°")
col4.markdown(
    f"<div style='font-size:22px; text-align:center'>{weather_description(current['weathercode'])}</div>",
    unsafe_allow_html=True
)

st.markdown("---")

st.subheader("📈 48-Hour Forecast")

hourly = data["hourly"]

df_hourly = pd.DataFrame({
    "Time": pd.to_datetime(hourly["time"][:48]),
    "Temperature": hourly["temperature_2m"][:48],
    "Rain Probability": hourly["precipitation_probability"][:48]
})

fig1 = px.line(
    df_hourly,
    x="Time",
    y="Temperature",
    title="🌡 Temperature Next 48 Hours",
    template="plotly_white",
    markers=True
)
fig1.update_traces(line=dict(color="#FF5733"), marker=dict(size=6))
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    df_hourly,
    x="Time",
    y="Rain Probability",
    title="🌧 Rain Probability (%)",
    template="plotly_white",
    color="Rain Probability",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.subheader("📅 7-Day Forecast")

daily = data["daily"]

df_daily = pd.DataFrame({
    "Date": pd.to_datetime(daily["time"]),
    "Max Temp": daily["temperature_2m_max"],
    "Min Temp": daily["temperature_2m_min"],
    "Rain (mm)": daily["precipitation_sum"],
    "Weather Code": daily["weathercode"]
})
df_daily["Condition"] = df_daily["Weather Code"].apply(weather_description)

fig3 = px.bar(
    df_daily,
    x="Date",
    y=["Max Temp", "Min Temp"],
    title="🌡 7-Day Temperature Forecast",
    template="plotly_white",
    barmode="group",
    color_discrete_sequence=["#FF5733", "#33CFFF"]
)
st.plotly_chart(fig3, use_container_width=True)


st.dataframe(df_daily[["Date", "Max Temp", "Min Temp", "Rain (mm)", "Condition"]])

st.markdown("---")

st.subheader("🤖 AI Temperature Prediction")

prediction = predict_temperature(df_hourly["Temperature"])
st.success(f"🔮 Predicted Next Hour Temperature: {prediction:.2f} °C")
