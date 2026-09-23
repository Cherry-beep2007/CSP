import os
import requests
import streamlit as st
from typing import Dict, Any, List, Optional

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_destination_images(query: str, count: int = 4) -> List[str]:
    """
    Fetches real high-quality photos for a destination/attraction using Unsplash API if available,
    or returns curated high-res travel photos dynamically matching the query.
    """
    api_key = os.getenv("UNSPLASH_ACCESS_KEY", "").strip()
    images = []

    if api_key:
        try:
            url = "https://api.unsplash.com/search/photos"
            params = {
                "query": f"{query} travel landmark destination",
                "per_page": count,
                "orientation": "landscape",
                "client_id": api_key
            }
            resp = requests.get(url, params=params, timeout=6)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                for item in results:
                    urls = item.get("urls", {})
                    img_url = urls.get("regular") or urls.get("small")
                    if img_url:
                        images.append(img_url)
        except Exception as e:
            print(f"Unsplash API fetch failed: {e}")

    # Fallback curated high quality travel photo bank if Unsplash API key is missing or fails
    fallback_pool = {
        "hampi": [
            "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1600100397608-f010e423b971?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=1200&q=80"
        ],
        "jaipur": [
            "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=1200&q=80"
        ],
        "varanasi": [
            "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=1200&q=80"
        ],
        "agra": [
            "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1585135497273-1a86b09fe70e?auto=format&fit=crop&w=1200&q=80"
        ],
        "rome": [
            "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?auto=format&fit=crop&w=1200&q=80"
        ],
        "paris": [
            "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1200&q=80"
        ],
        "kyoto": [
            "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?auto=format&fit=crop&w=1200&q=80"
        ],
        "nature": [
            "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1426604966848-d7adac402bff?auto=format&fit=crop&w=1200&q=80"
        ],
        "heritage": [
            "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80"
        ]
    }

    if not images:
        q_lower = query.strip().lower()
        for key in fallback_pool:
            if key in q_lower:
                images = fallback_pool[key]
                break

    if not images:
        images = [
            "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80"
        ]

    return images[:count]

def get_hero_image(destination: str) -> str:
    """Returns a single hero background image URL for destination."""
    imgs = fetch_destination_images(destination, count=1)
    return imgs[0] if imgs else "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1200&q=80"
