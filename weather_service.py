import requests
import streamlit as st
from typing import Dict, Any, Optional, List

WEATHER_CODES = {
    0: ("Clear Sky", "☀️", "Ideal for outdoor sightseeing, photography and heritage walks."),
    1: ("Mainly Clear", "🌤️", "Great weather for outdoor exploration."),
    2: ("Partly Cloudy", "⛅", "Pleasant weather for all travel activities."),
    3: ("Overcast", "☁️", "Good conditions for exploring outdoor and historical sites."),
    45: ("Foggy", "🌫️", "Drive carefully; great time for morning tea and heritage cafes."),
    48: ("Depositing Rime Fog", "🌫️", "Cool foggy weather."),
    51: ("Light Drizzle", "🌦️", "Carry a light umbrella or rain jacket."),
    53: ("Moderate Drizzle", "🌦️", "Consider visiting indoor museums and covered heritage palaces."),
    55: ("Dense Drizzle", "🌧️", "Rain expected; indoor heritage locations recommended."),
    61: ("Slight Rain", "🌧️", "Carry an umbrella. Excellent time for museum visits."),
    63: ("Moderate Rain", "🌧️", "Rainy weather. Prioritize indoor art galleries, cafes and indoor sites."),
    65: ("Heavy Rain", "⛈️", "Heavy rain expected! Plan indoor cultural activities and cozy dining."),
    71: ("Slight Snow", "🌨️", "Dress warm! Beautiful winter landscape views."),
    73: ("Moderate Snow", "🌨️", "Bundle up in layers for outdoor snow activities."),
    75: ("Heavy Snow", "❄️", "Extreme snow conditions. Stay safe and enjoy indoor warmth."),
    80: ("Rain Showers", "🌦️", "Intermittent showers expected."),
    95: ("Thunderstorm", "🌩️", "Thunderstorms reported. Avoid open high-altitude viewpoints.")
}

@st.cache_data(ttl=14400, show_spinner=False)
def fetch_weather_forecast(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """
    Fetches 7-day daily weather forecast from Open-Meteo API.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "weathercode",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "windspeed_10m_max"
        ],
        "current_weather": True,
        "timezone": "auto"
    }

    try:
        resp = requests.get(url, params=params, timeout=6)
        if resp.status_code == 200:
            data = resp.json()
            curr = data.get("current_weather", {})
            curr_code = curr.get("weathercode", 0)
            code_info = WEATHER_CODES.get(curr_code, ("Fair", "🌤️", "Enjoy your day."))

            daily = data.get("daily", {})
            forecast_list = []
            dates = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            codes = daily.get("weathercode", [])
            precip_prob = daily.get("precipitation_probability_max", [])
            wind = daily.get("windspeed_10m_max", [])

            rain_alert = False
            for i in range(min(len(dates), 7)):
                d_code = codes[i] if i < len(codes) else 0
                d_info = WEATHER_CODES.get(d_code, ("Fair", "🌤️", "Good day for sightseeing."))
                p_prob = precip_prob[i] if i < len(precip_prob) else 0
                if p_prob > 40 or d_code in [51, 53, 55, 61, 63, 65, 80, 95]:
                    rain_alert = True

                forecast_list.append({
                    "date": dates[i],
                    "max_temp": max_temps[i] if i < len(max_temps) else 25,
                    "min_temp": min_temps[i] if i < len(min_temps) else 18,
                    "code": d_code,
                    "condition": d_info[0],
                    "icon": d_info[1],
                    "precip_prob": p_prob,
                    "wind_speed": wind[i] if i < len(wind) else 10,
                    "tip": d_info[2]
                })

            travel_tip = "Weather looks pleasant for exploring heritage monuments and outdoor sights."
            if rain_alert:
                travel_tip = "Rain is likely during your trip! TripGenie recommends prioritizing indoor heritage museums, royal palaces, and local art centers during rainy hours."
            elif curr.get("temperature", 25) > 34:
                travel_tip = "High temperatures expected. Plan outdoor monuments early morning or late afternoon, and stay hydrated."

            return {
                "current_temp": curr.get("temperature", 24),
                "current_condition": code_info[0],
                "current_icon": code_info[1],
                "wind_speed": curr.get("windspeed", 10),
                "travel_tip": travel_tip,
                "rain_alert": rain_alert,
                "daily_forecast": forecast_list
            }
    except Exception as e:
        print(f"Weather API error for ({lat}, {lon}): {e}")

    # Default fallback weather response
    return {
        "current_temp": 24.5,
        "current_condition": "Partly Cloudy",
        "current_icon": "⛅",
        "wind_speed": 12.0,
        "travel_tip": "Check local forecast upon arrival; pleasant temperatures expected for heritage tours.",
        "rain_alert": False,
        "daily_forecast": [
            {
                "date": "Day 1",
                "max_temp": 28,
                "min_temp": 18,
                "code": 2,
                "condition": "Partly Cloudy",
                "icon": "⛅",
                "precip_prob": 10,
                "wind_speed": 12,
                "tip": "Great weather for outdoor exploration."
            }
        ]
    }
