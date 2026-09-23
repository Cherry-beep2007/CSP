import requests
import streamlit as st
from typing import Dict, Any, Optional

USER_AGENT = "TripGenie-TravelApp/1.0 (Community Tourism Project; contact@tripgenie.app)"

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_wikipedia_summary(query: str) -> Optional[Dict[str, Any]]:
    """
    Fetches Wikipedia page summary, thumbnail image, and page URL.
    """
    if not query:
        return None

    clean_query = query.strip()
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(clean_query)}"
    headers = {"User-Agent": USER_AGENT}

    try:
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code == 200:
            data = response.json()
            extract = data.get("extract", "")
            thumbnail = data.get("thumbnail", {}).get("source") if "thumbnail" in data else None
            page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")

            if extract:
                return {
                    "title": data.get("title", clean_query),
                    "extract": extract,
                    "description": data.get("description", "Famous travel & heritage destination"),
                    "thumbnail": thumbnail,
                    "url": page_url
                }
    except Exception as e:
        print(f"Wikipedia fetch error for {query}: {e}")

    # Search fallback if exact page title title-cased didn't match directly
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(clean_query)}&format=json"
        sr_resp = requests.get(search_url, headers=headers, timeout=6)
        if sr_resp.status_code == 200:
            sr_data = sr_resp.json()
            search_results = sr_data.get("query", {}).get("search", [])
            if search_results:
                top_title = search_results[0]["title"]
                # Fetch summary for top search title
                res_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(top_title)}"
                res_resp = requests.get(res_url, headers=headers, timeout=6)
                if res_resp.status_code == 200:
                    d = res_resp.json()
                    return {
                        "title": d.get("title", top_title),
                        "extract": d.get("extract", ""),
                        "description": d.get("description", "Travel & heritage destination"),
                        "thumbnail": d.get("thumbnail", {}).get("source") if "thumbnail" in d else None,
                        "url": d.get("content_urls", {}).get("desktop", {}).get("page", "")
                    }
    except Exception as e:
        print(f"Wikipedia search fallback error: {e}")

    return None
