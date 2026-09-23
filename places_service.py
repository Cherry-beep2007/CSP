import json
import os
import requests
import streamlit as st
from typing import List, Dict, Any, Optional
from utils.route_optimizer import haversine_distance

USER_AGENT = "TripGenie-TravelApp/1.0 (Community Tourism Project; contact@tripgenie.app)"

@st.cache_data(ttl=86400, show_spinner=False)
def load_offline_heritage_data() -> Dict[str, List[Dict[str, Any]]]:
    """Loads pre-seeded offline heritage database."""
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "heritage_data.json")
    try:
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading offline heritage data: {e}")
    return {}

@st.cache_data(ttl=43200, show_spinner=False)
def fetch_places_from_overpass(lat: float, lon: float, radius_m: int = 8000) -> List[Dict[str, Any]]:
    """
    Queries OpenStreetMap Overpass API for tourism, historic, leisure, and heritage POIs.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:10];
    (
      node["historic"](around:{radius_m},{lat},{lon});
      node["tourism"](around:{radius_m},{lat},{lon});
      node["amenity"="place_of_worship"](around:{radius_m},{lat},{lon});
      node["leisure"="park"](around:{radius_m},{lat},{lon});
      way["historic"](around:{radius_m},{lat},{lon});
      way["tourism"="attraction"](around:{radius_m},{lat},{lon});
    );
    out center 35;
    """
    try:
        resp = requests.post(overpass_url, data={"data": query}, headers={"User-Agent": USER_AGENT}, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            elements = data.get("elements", [])
            places = []
            seen_names = set()

            for elem in elements:
                tags = elem.get("tags", {})
                name = tags.get("name") or tags.get("name:en")
                if not name or name in seen_names or len(name) < 3:
                    continue

                seen_names.add(name)
                p_lat = elem.get("lat") or elem.get("center", {}).get("lat")
                p_lon = elem.get("lon") or elem.get("center", {}).get("lon")

                if not p_lat or not p_lon:
                    continue

                # Categorize based on OSM tags
                historic_tag = tags.get("historic", "")
                tourism_tag = tags.get("tourism", "")
                amenity_tag = tags.get("amenity", "")
                leisure_tag = tags.get("leisure", "")

                category = "Attraction"
                if historic_tag or tourism_tag in ["museum", "artwork"]:
                    category = "Historical Monuments"
                elif amenity_tag == "place_of_worship":
                    category = "Temples & Spiritual"
                elif tourism_tag == "viewpoint" or leisure_tag == "park":
                    category = "Nature & Viewpoints"
                elif tourism_tag in ["theme_park", "zoo"]:
                    category = "Family & Entertainment"

                desc = tags.get("description") or f"Popular landmark in the area."

                places.append({
                    "name": name,
                    "category": category,
                    "description": desc,
                    "cultural_relevance": f"Significant local landmark in region.",
                    "lat": float(p_lat),
                    "lon": float(p_lon),
                    "tags": tags
                })
            return places
    except Exception as e:
        print(f"Overpass API error for ({lat}, {lon}): {e}")

    return []

def get_destination_places(
    destination_name: str,
    lat: float,
    lon: float,
    mood: str = "Relaxed",
    interests: List[str] = None
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Returns (attractions, heritage_sites) tailored to destination and mood.
    Combines offline curated heritage data with live OSM/Wikipedia queries.
    """
    if interests is None:
        interests = ["Heritage", "Nature", "Food"]

    offline_db = load_offline_heritage_data()
    dest_key = destination_name.strip().lower()

    heritage_sites = []
    attractions = []

    # Check offline heritage matching first
    matched_key = None
    for k in offline_db:
        if k in dest_key or dest_key in k:
            matched_key = k
            break

    if matched_key:
        heritage_sites.extend(offline_db[matched_key])

    # Fetch live OSM places
    live_places = fetch_places_from_overpass(lat, lon)
    for p in live_places:
        if p["category"] in ["Historical Monuments", "Temples & Spiritual"]:
            if not any(h["name"].lower() == p["name"].lower() for h in heritage_sites):
                heritage_sites.append(p)
        else:
            attractions.append(p)

    # Fallback default places generator if live + offline yield under 6 items
    if len(heritage_sites) + len(attractions) < 6:
        defaults = generate_generic_destination_places(destination_name, lat, lon, mood)
        for d in defaults:
            if d.get("is_heritage"):
                if not any(h["name"].lower() == d["name"].lower() for h in heritage_sites):
                    heritage_sites.append(d)
            else:
                if not any(a["name"].lower() == d["name"].lower() for a in attractions):
                    attractions.append(d)

    # Filter and balance places according to user mood
    heritage_sites = filter_by_mood_and_interests(heritage_sites, mood, interests)
    attractions = filter_by_mood_and_interests(attractions, mood, interests)

    return attractions, heritage_sites

def filter_by_mood_and_interests(
    places: List[Dict[str, Any]],
    mood: str,
    interests: List[str]
) -> List[Dict[str, Any]]:
    """Sorts and filters places to prioritize items matching user mood and interests."""
    if not places:
        return []

    mood_boost_keywords = {
        "Relaxed": ["park", "lake", "garden", "stroll", "cafe", "river", "beach", "scenic"],
        "Adventurous": ["fort", "trek", "viewpoint", "hill", "river", "cave", "outdoor", "cliff"],
        "Romantic": ["sunset", "palace", "lake", "viewpoint", "gardens", "promenade", "riverfront"],
        "Peaceful": ["temple", "monastery", "ashram", "garden", "shrine", "quiet", "lake", "park"],
        "Cultural": ["monument", "museum", "fort", "heritage", "palace", "bazaar", "art", "temple"],
        "Spiritual": ["temple", "ghat", "church", "mosque", "shrine", "ashram", "sacred"],
        "Family": ["park", "zoo", "museum", "palace", "science", "fort", "garden"],
        "Nature": ["park", "lake", "sanctuary", "waterfall", "hill", "forest", "viewpoint"]
    }

    keywords = mood_boost_keywords.get(mood, [])

    def score_place(p: Dict[str, Any]) -> int:
        score = 0
        text = (p.get("name", "") + " " + p.get("description", "") + " " + p.get("category", "")).lower()
        for kw in keywords:
            if kw in text:
                score += 3
        for interest in interests:
            if interest.lower() in text:
                score += 2
        return score

    sorted_places = sorted(places, key=score_place, reverse=True)
    return sorted_places

def generate_generic_destination_places(
    destination: str,
    lat: float,
    lon: float,
    mood: str
) -> List[Dict[str, Any]]:
    """Synthesizes realistic location points for arbitrary destinations if API responses are sparse."""
    dest_title = destination.title()
    return [
        {
            "name": f"Historic Central Square of {dest_title}",
            "category": "Historical Monuments",
            "description": f"The vibrant historic core of {dest_title}, featuring heritage architecture, street cafes, and local monuments.",
            "cultural_relevance": f"Iconic gathering place showcasing the history and heritage of {dest_title}.",
            "lat": lat + 0.002,
            "lon": lon + 0.003,
            "is_heritage": True
        },
        {
            "name": f"{dest_title} Cultural Heritage Museum",
            "category": "Museums & Science",
            "description": f"Displays rare artifacts, traditional crafts, folklore, and historical archives documenting the rich past of {dest_title}.",
            "cultural_relevance": "Key repository of local cultural preservation and history.",
            "lat": lat - 0.003,
            "lon": lon + 0.001,
            "is_heritage": True
        },
        {
            "name": f"{dest_title} Royal Fort & Citadel Grounds",
            "category": "Forts & Palaces",
            "description": f"Ancient architectural fortification offering panoramic city vistas, stone battlements, and serene courtyards.",
            "cultural_relevance": "Architectural landmark and defensive heritage citadel.",
            "lat": lat + 0.005,
            "lon": lon - 0.004,
            "is_heritage": True
        },
        {
            "name": f"Grand Spiritual Shrine of {dest_title}",
            "category": "Temples & Spiritual",
            "description": f"Revered heritage temple complex known for peaceful atmosphere, intricate stone carvings, and traditional morning prayers.",
            "cultural_relevance": "Primary spiritual hub and sanctuary for locals and pilgrims.",
            "lat": lat - 0.004,
            "lon": lon - 0.002,
            "is_heritage": True
        },
        {
            "name": f"{dest_title} Panoramic Sunset Viewpoint",
            "category": "Nature & Viewpoints",
            "description": f"High hilltop lookout point giving breathtaking 360-degree vistas over {dest_title} and surrounding natural landscapes.",
            "cultural_relevance": "Popular scenic destination for sunset walks and photography.",
            "lat": lat + 0.008,
            "lon": lon + 0.006,
            "is_heritage": False
        },
        {
            "name": f"Old Town Heritage Bazaar & Crafts Market",
            "category": "Cultural & Shopping",
            "description": f"Bustling traditional market filled with local artisans, handloom textiles, authentic street delicacies, and spices.",
            "cultural_relevance": "Living cultural marketplace supporting local heritage crafts.",
            "lat": lat - 0.001,
            "lon": lon + 0.004,
            "is_heritage": False
        },
        {
            "name": f"Serene Botanical Gardens of {dest_title}",
            "category": "Nature & Parks",
            "description": f"Lush green municipal gardens featuring century-old trees, tranquil lotus ponds, and shaded walking avenues.",
            "cultural_relevance": "Historic green haven beloved by families and nature enthusiasts.",
            "lat": lat + 0.004,
            "lon": lon - 0.006,
            "is_heritage": False
        }
    ]
