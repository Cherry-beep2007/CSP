import streamlit as st
from typing import List, Dict, Any

def render_itinerary_timeline(itinerary_data: List[Dict[str, Any]]):
    """Renders the day-wise timeline with slot cards, travel times, and activity recommendations."""
    if not itinerary_data:
        st.info("No itinerary generated yet.")
        return

    st.markdown("### 🗓️ Day-by-Day Personalized Itinerary")

    for day_info in itinerary_data:
        day_num = day_info.get("day", 1)
        theme = day_info.get("theme", f"Day {day_num}")
        slots = day_info.get("slots", [])

        with st.expander(f"📌 **Day {day_num}: {theme}**", expanded=(day_num == 1)):
            for slot in slots:
                period = slot.get("period", "Morning")
                place = slot.get("place", "Local Landmark")
                category = slot.get("category", "Attraction")
                activity = slot.get("activity", "")
                duration = slot.get("duration", "2-3 hrs")
                reason = slot.get("reason", "")
                dist_km = slot.get("distance_km", "N/A")
                ttime = slot.get("travel_time", "")

                # Badge colors
                badge_class = "tg-badge-primary"
                if "Historical" in category or "Heritage" in category:
                    badge_class = "tg-badge-heritage"
                elif "Temples" in category or "Spiritual" in category:
                    badge_class = "tg-badge-accent"

                st.markdown(
                    f"""
                    <div class="tg-timeline-slot">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <h4 style="margin: 0; color: #38bdf8;">{period} &bull; {place}</h4>
                            <span class="tg-badge {badge_class}">{category}</span>
                        </div>
                        <p style="margin: 0.4rem 0 0.6rem 0; color: #cbd5e1; font-size: 0.92rem; line-height: 1.5;">
                            {activity}
                        </p>
                        <div style="display: flex; gap: 1.5rem; font-size: 0.82rem; color: #94a3b8; background: rgba(15, 23, 42, 0.5); padding: 0.5rem 0.8rem; border-radius: 8px;">
                            <span>⏱️ <b>Duration:</b> {duration}</span>
                            <span>🚗 <b>Distance:</b> {dist_km} km</span>
                            <span>🚘 <b>Est Travel:</b> {ttime}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #fbbf24; margin-top: 0.4rem;">
                            💡 <i>{reason}</i>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
