import streamlit as st
from typing import List, Dict, Any

def render_heritage_section(heritage_data: List[Dict[str, Any]], destination_name: str):
    """Renders the dedicated Local Heritage & Culture grid section."""
    st.markdown(f"### 🏛️ Local Heritage & Cultural Discovery in {destination_name.title()}")
    st.markdown(
        """
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem;">
            Explore significant historical monuments, ancient shrines, royal citadels, and traditional craft markets. 
            Promoting awareness and preservation of local heritage.
        </p>
        """,
        unsafe_allow_html=True
    )

    if not heritage_data:
        st.info("No heritage records retrieved for this destination.")
        return

    cols = st.columns(2)
    for idx, site in enumerate(heritage_data):
        col = cols[idx % 2]
        name = site.get("name", "Heritage Landmark")
        cat = site.get("category", "Historical Site")
        desc = site.get("description", "A notable historical landmark in the region.")
        rel = site.get("cultural_relevance", "Key local heritage landmark.")
        img = site.get("image") or "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80"
        lat = site.get("lat")
        lon = site.get("lon")

        with col:
            st.markdown(
                f"""
                <div class="tg-card">
                    <div style="border-radius: 10px; overflow: hidden; height: 160px; margin-bottom: 1rem;">
                        <img src="{img}" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <h4 style="margin: 0; color: #f8fafc;">{name}</h4>
                        <span class="tg-badge tg-badge-heritage">{cat}</span>
                    </div>
                    <p style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 0.6rem; line-height: 1.4;">
                        {desc}
                    </p>
                    <div style="font-size: 0.82rem; color: #fbbf24; background: rgba(251, 191, 36, 0.1); padding: 0.5rem 0.75rem; border-radius: 8px; margin-bottom: 0.6rem;">
                        <b>Cultural Significance:</b> {rel}
                    </div>
                    <div style="font-size: 0.78rem; color: #64748b;">
                        📍 Coordinates: {lat:.4f}, {lon:.4f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
