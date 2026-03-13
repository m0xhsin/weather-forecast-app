def weather_description(code):
    mapping = {
        0: "☀️ Clear Sky",
        1: "🌤 Mainly Clear",
        2: "⛅ Partly Cloudy",
        3: "☁️ Overcast",
        45: "🌫 Fog",
        48: "🌫 Depositing Rime Fog",
        51: "🌦 Light Drizzle",
        61: "🌧 Light Rain",
        63: "🌧 Moderate Rain",
        65: "🌧 Heavy Rain",
        71: "❄️ Snow",
        80: "🌦 Rain Showers",
        95: "⛈ Thunderstorm"
    }

    return mapping.get(code, "Unknown")
