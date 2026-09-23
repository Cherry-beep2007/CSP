import math
import random
from typing import List, Dict, Any, Tuple
from utils.route_optimizer import optimize_place_sequence, haversine_distance, estimate_travel_time

def generate_personalized_itinerary(
    destination: str,
    duration: int,
    mood: str,
    travel_style: str,
    budget: str,
    interests: List[str],
    all_places: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generates a structured, multi-day personalized itinerary split into Morning, Afternoon, and Evening.
    Prevents duplicate places and optimizes geographic routes day by day.
    """
    if not all_places:
        all_places = []

    # Copy list to track used places
    pool = [dict(p) for p in all_places]
    
    # Shuffle slightly with seed based on destination for stability
    random.seed(len(destination) + duration + len(mood))

    # Day themes based on mood and duration
    themes = get_day_themes(destination, duration, mood)

    itinerary = []
    used_names = set()

    for d in range(1, duration + 1):
        day_theme = themes[d - 1] if d - 1 < len(themes) else f"Discovering {destination} - Day {d}"
        
        # Pick 3 suitable distinct places for Morning, Afternoon, Evening
        available_pool = [p for p in pool if p.get('name') not in used_names]
        
        # If pool exhausted, recycle gracefully with slight variations
        if len(available_pool) < 3:
            available_pool = pool.copy()

        # Sequence available pool for geographic proximity
        sequenced = optimize_place_sequence(available_pool[:8])

        day_places = []
        for p in sequenced:
            if p.get('name') not in used_names:
                day_places.append(p)
                used_names.add(p.get('name'))
            if len(day_places) == 3:
                break

        # Fallback if still under 3
        while len(day_places) < 3:
            dummy = {
                "name": f"{destination} Scenic Promenade",
                "category": "Scenic & Leisure",
                "description": f"Enjoy local street life, heritage architecture, and tea shops.",
                "cultural_relevance": "Local atmosphere.",
                "lat": pool[0]['lat'] + random.uniform(-0.01, 0.01) if pool else 0,
                "lon": pool[0]['lon'] + random.uniform(-0.01, 0.01) if pool else 0
            }
            day_places.append(dummy)

        # Build 3 time slots
        slots = []
        periods = [
            ("morning", "Morning (09:00 AM - 12:30 PM)", "2-3 hrs"),
            ("afternoon", "Afternoon (01:30 PM - 05:00 PM)", "2-3.5 hrs"),
            ("evening", "Evening (05:30 PM - 08:30 PM)", "2-3 hrs")
        ]

        prev_place = None
        for i, (period_key, period_label, duration_str) in enumerate(periods):
            place = day_places[i]
            activity = build_activity_description(place, period_key, mood, travel_style)
            reason = build_recommendation_reason(place, mood, interests)

            dist_km = "N/A"
            ttime = "Local spot"
            if prev_place and prev_place.get('lat') and place.get('lat'):
                d_val = haversine_distance(prev_place['lat'], prev_place['lon'], place['lat'], place['lon'])
                dist_km = round(d_val, 1)
                ttime = estimate_travel_time(dist_km)

            slots.append({
                "period": period_label,
                "place": place['name'],
                "category": place.get('category', 'Attraction'),
                "activity": activity,
                "duration": duration_str,
                "reason": reason,
                "distance_km": dist_km,
                "travel_time": ttime,
                "lat": place.get('lat'),
                "lon": place.get('lon'),
                "description": place.get('description', ''),
                "cultural_relevance": place.get('cultural_relevance', '')
            })

            prev_place = place

        itinerary.append({
            "day": d,
            "theme": day_theme,
            "slots": slots
        })

    return itinerary

def get_day_themes(destination: str, duration: int, mood: str) -> List[str]:
    """Generates thematic titles for each day based on mood."""
    mood_themes = {
        "Relaxed": ["Heritage & Scenic Strolls", "Lakes, Gardens & Cafes", "Local Art & Slow Dining", "Unwind & Sunset Views"],
        "Adventurous": ["Historic Citadel & Heights", "Trail Exploration & Forts", "Outdoor Wonders", "Vanguard Heritage Quest"],
        "Romantic": ["Palace Elegance & Sunset Vistas", "Old Quarter Romance", "Scenic Promenade & Fine Dining", "Quiet Gardens & Heritage"],
        "Peaceful": ["Sacred Shrines & Morning Quiet", "Spiritual Heritage Walk", "Serene Nature & Reflection", "Tranquil Garden Experience"],
        "Cultural": ["Grand Monuments & History", "Museums & Local Artisans", "Fortress Architecture", "Traditional Crafts & Heritage"],
        "Spiritual": ["Holy Shrines & Morning Rituals", "Temple Heritage & Chantings", "Sacred Waters & Reflection", "Peaceful Ashram Walk"],
        "Family": ["Family Heritage Landmarks", "Parks, Museums & Interactive Tours", "Historic Forts & Fun Spots", "Local Markets & Snacks"],
        "Nature": ["Botanical Wonders & Green Trails", "Hilltop Views & Riverbanks", "Nature Sanctuaries & Parks", "Open Air Heritage"]
    }
    base = mood_themes.get(mood, mood_themes["Relaxed"])
    result = []
    for i in range(duration):
        if i < len(base):
            result.append(f"{base[i]} in {destination.title()}")
        else:
            result.append(f"Exploring Heritage & Hidden Gems - Day {i+1}")
    return result

def build_activity_description(place: Dict[str, Any], period: str, mood: str, style: str) -> str:
    """Creates a vivid activity description based on place, time of day, and travel style."""
    p_name = place.get('name', 'landmark')
    cat = place.get('category', 'attraction')
    desc = place.get('description', '')

    if period == "morning":
        return f"Start your morning with a guided tour of {p_name}. Explore the early architecture, capture morning photos, and absorb {desc}"
    elif period == "afternoon":
        return f"Head to {p_name} for an afternoon immersive visit ({cat}). Take time to read historical plaques, enjoy nearby local snacks, and admire {desc}"
    else:
        return f"Conclude your day at {p_name}. Experience the evening ambience, golden hour photography, and local atmosphere with {style.lower()} companions."

def build_recommendation_reason(place: Dict[str, Any], mood: str, interests: List[str]) -> str:
    """Generates explicit explanation for why this place was recommended."""
    cat = place.get('category', 'attraction')
    if "Historical" in cat or "Heritage" in cat:
        return f"Matches your interest in local heritage and cultural preservation."
    elif "Temples" in cat or "Spiritual" in cat:
        return f"Recommended for a peaceful, reflective experience tailored to a {mood.lower()} trip."
    elif "Nature" in cat or "Parks" in cat:
        return f"Fits your {mood.lower()} travel style with serene green spaces and views."
    else:
        return f"Handpicked highlight aligning with your choice of {mood.lower()} trip."

def calculate_budget_estimate(
    duration: int,
    budget_tier: str,
    travel_style: str
) -> Dict[str, Any]:
    """Calculates realistic estimated trip budget breakdown in INR / USD."""
    # Per day base rates per person in INR
    multiplier = 1.0
    if travel_style == "Couple":
        multiplier = 1.8
    elif travel_style == "Family":
        multiplier = 3.2
    elif travel_style == "Friends":
        multiplier = 2.4

    if budget_tier == "Budget":
        acc_per_day = 1200 * multiplier
        food_per_day = 600 * multiplier
        trans_per_day = 400 * multiplier
        entry_per_day = 300 * multiplier
        misc_per_day = 250 * multiplier
    elif budget_tier == "Luxury":
        acc_per_day = 7500 * multiplier
        food_per_day = 2500 * multiplier
        trans_per_day = 2000 * multiplier
        entry_per_day = 1000 * multiplier
        misc_per_day = 1000 * multiplier
    else: # Moderate
        acc_per_day = 3200 * multiplier
        food_per_day = 1200 * multiplier
        trans_per_day = 800 * multiplier
        entry_per_day = 500 * multiplier
        misc_per_day = 500 * multiplier

    acc_total = acc_per_day * duration
    food_total = food_per_day * duration
    trans_total = trans_per_day * duration
    entry_total = entry_per_day * duration
    misc_total = misc_per_day * duration

    total = acc_total + food_total + trans_total + entry_total + misc_total

    return {
        "currency": "INR",
        "total_estimated": total,
        "breakdown": {
            "Accommodation": acc_total,
            "Food & Dining": food_total,
            "Local Transportation": trans_total,
            "Entry Fees & Activities": entry_total,
            "Miscellaneous & Souvenirs": misc_total
        },
        "budget_tier": budget_tier,
        "travel_style": travel_style
    }
