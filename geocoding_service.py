import requests
import streamlit as st
from typing import Dict, Any, Optional

USER_AGENT = "TripGenie-TravelApp/1.0 (Community Tourism Project; contact@tripgenie.app)"

@st.cache_data(ttl=86400, show_spinner=False)
def geocode_destination(destination_name: str) -> Optional[Dict[str, Any]]:
    """
    Geocodes a destination name using OpenStreetMap Nominatim API.
    Returns lat, lon, display_name, address, boundingbox or None.
    """
    if not destination_name or not destination_name.strip():
        return None

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": destination_name.strip(),
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                result = data[0]
                return {
                    "name": destination_name.strip().title(),
                    "display_name": result.get("display_name", destination_name),
                    "lat": float(result.get("lat")),
                    "lon": float(result.get("lon")),
                    "type": result.get("type", "city"),
                    "boundingbox": result.get("boundingbox", []),
                    "address": result.get("address", {})
                }
    except Exception as e:
        print(f"Geocoding error for {destination_name}: {e}")

    # Fallback coordinates for common popular destinations if offline/failed
    fallback_map = {
        "hampi": {"name": "Hampi", "lat": 15.3350, "lon": 76.4600, "display_name": "Hampi, Karnataka, India"},
        "jaipur": {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873, "display_name": "Jaipur, Rajasthan, India"},
        "varanasi": {"name": "Varanasi", "lat": 25.3176, "lon": 82.9739, "display_name": "Varanasi, Uttar Pradesh, India"},
        "agra": {"name": "Agra", "lat": 27.1767, "lon": 78.0081, "display_name": "Agra, Uttar Pradesh, India"},
        "mysuru": {"name": "Mysuru", "lat": 12.2958, "lon": 76.6394, "display_name": "Mysuru, Karnataka, India"},
        "mysore": {"name": "Mysore", "lat": 12.2958, "lon": 76.6394, "display_name": "Mysuru, Karnataka, India"},
        "delhi": {"name": "Delhi", "lat": 28.6139, "lon": 77.2090, "display_name": "New Delhi, Delhi, India"},
        "paris": {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "display_name": "Paris, Île-de-France, France"},
        "rome": {"name": "Rome", "lat": 41.9028, "lon": 12.4964, "display_name": "Rome, Lazio, Italy"},
        "kyoto": {"name": "Kyoto", "lat": 35.0116, "lon": 135.7681, "display_name": "Kyoto, Japan"},
        "london": {"name": "London", "lat": 51.5074, "lon": -0.1278, "display_name": "London, England, UK"},
    }
    
    key = destination_name.strip().lower()
    if key in fallback_map:
        fb = fallback_map[key]
        return {
            "name": fb["name"],
            "display_name": fb["display_name"],
            "lat": fb["lat"],
            "lon": fb["lon"],
            "type": "city",
            "boundingbox": [],
            "address": {}
        }

    return None
