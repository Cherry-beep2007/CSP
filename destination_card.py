import streamlit as st
from typing import Dict, Any, List

def render_destination_overview(
    destination_info: Dict[str, Any],
    wiki_info: Dict[str, Any],
    images: List[str]
):
    """Renders the top Destination Overview card with real imagery and Wikipedia details."""
    dest_name = destination_info.get("name", "Destination")
    display_name = destination_info.get("display_name", dest_name)
    lat = destination_info.get("lat")
    lon = destination_info.get("lon")

    col_img, col_info = st.columns([1.2, 1.8])

    with col_img:
        hero_img = images[0] if images else "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80"
        st.markdown(
            f"""
            <div style="border-radius: 14px; overflow: hidden; height: 260px; box-shadow: 0 8px 20px rgba(0,0,0,0.4);">
                <img src="{hero_img}" style="width: 100%; height: 100%; object-fit: cover;" alt="{dest_name}">
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_info:
        st.markdown(f"## 📍 {dest_name}")
        st.markdown(f"**Location:** `{display_name}`")
        st.markdown(f"**Coordinates:** `Lat {lat:.4f}, Lon {lon:.4f}`")

        if wiki_info:
            extract = wiki_info.get("extract", "")
            if len(extract) > 320:
                extract = extract[:320] + "..."
            st.markdown(f"*{extract}*")
            if wiki_info.get("url"):
                st.markdown(f"🔗 [Read full Wikipedia history]({wiki_info['url']})")
        else:
            st.markdown(f"*{dest_name} is a renowned travel hub known for its historical landmarks, scenic vistas, and rich local heritage.*")

    # Image Gallery Strip
    if len(images) > 1:
        st.markdown("#### 📸 Destination Highlights")
        g_cols = st.columns(min(len(images) - 1, 3))
        for idx, img_url in enumerate(images[1:4]):
            with g_cols[idx]:
                st.markdown(
                    f"""
                    <div style="border-radius: 10px; overflow: hidden; height: 120px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                        <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
