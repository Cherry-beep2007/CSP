import math
from typing import List, Dict, Any, Tuple

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees).
    """
    R = 6371.0  # Radius of Earth in km
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) *
         math.sin(delta_lambda / 2.0) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def estimate_travel_time(distance_km: float) -> str:
    """
    Provides a human-readable estimate of travel time based on distance.
    Assuming average urban travel speed of 25-35 km/h.
    """
    if distance_km <= 0.5:
        return "~5-10 min walk"
    elif distance_km <= 2.0:
        return f"~{int(distance_km * 8)} min walk / 5 min ride"
    elif distance_km <= 10.0:
        mins = max(10, int(distance_km * 2.5))
        return f"~{mins} mins drive/taxi"
    elif distance_km <= 30.0:
        mins = int(distance_km * 2)
        return f"~{mins} mins drive"
    else:
        hours = round(distance_km / 45.0, 1)
        return f"~{hours} hours travel"

def optimize_place_sequence(places: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Simple Nearest Neighbor heuristic to sequence places to reduce backtracking.
    Each place dict should contain 'lat' and 'lon'.
    """
    if not places or len(places) <= 2:
        return places

    # Filter places with valid lat/lon
    valid_places = [p for p in places if p.get('lat') is not None and p.get('lon') is not None]
    invalid_places = [p for p in places if p not in valid_places]

    if not valid_places:
        return places

    unvisited = valid_places.copy()
    optimized = []
    
    # Start with the first place
    current = unvisited.pop(0)
    optimized.append(current)

    while unvisited:
        nearest_idx = 0
        min_dist = float('inf')
        
        c_lat, c_lon = current['lat'], current['lon']
        for idx, candidate in enumerate(unvisited):
            dist = haversine_distance(c_lat, c_lon, candidate['lat'], candidate['lon'])
            if dist < min_dist:
                min_dist = dist
                nearest_idx = idx

        current = unvisited.pop(nearest_idx)
        optimized.append(current)

    # Append places that lacked coordinates at the end
    return optimized + invalid_places
