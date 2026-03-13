from fastapi import FastAPI
import requests
import pandas as pd

app = FastAPI()

cities_df = pd.read_csv("cities.csv")

@app.get("/")
def home():
    return {"message": "Germany Weather API running"}

@app.get("/cities")
def get_cities():
    return cities_df["city"].unique().tolist()[:500]

@app.get("/weather/{city}")
def get_weather(city: str):

    city_data = cities_df[cities_df["city"].str.lower() == city.lower()]

    if city_data.empty:
        return {"error": "City not found"}

    lat = city_data.iloc[0]["lat"]
    lon = city_data.iloc[0]["lng"]

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=temperature_2m,relativehumidity_2m,"
        f"apparent_temperature,precipitation_probability,"
        f"weathercode"
        f"&daily=temperature_2m_max,temperature_2m_min,"
        f"precipitation_sum,weathercode"
        f"&timezone=auto"
    )

    response = requests.get(url)
    return response.json()
