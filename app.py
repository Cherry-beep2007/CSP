import os
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="TRIPGENIE - Smart Gateway to Your Destination",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import utils & services
from utils.cache import init_session_state, get_state, set_state, clear_trip_state
from utils.validators import validate_trip_inputs, sanitize_text
from utils.pdf_generator import generate_itinerary_pdf

from services.geocoding_service import geocode_destination
from services.wikipedia_service import fetch_wikipedia_summary
from services.image_service import fetch_destination_images, get_hero_image
from services.weather_service import fetch_weather_forecast
from services.places_service import get_destination_places
from services.itinerary_service import generate_personalized_itinerary, calculate_budget_estimate

from components.styles import inject_custom_css
from components.header import render_header
from components.hero import render_hero
from components.destination_card import render_destination_overview
from components.itinerary_card import render_itinerary_timeline
from components.heritage_card import render_heritage_section
from components.weather_card import render_weather_widget
from components.chatbot import render_chatbot

def main():
    # Initialize session state & inject custom CSS styling
    init_session_state()
    inject_custom_css()

    # Check for demo destination trigger from hero button
    if "demo_destination" in st.session_state and st.session_state["demo_destination"]:
        demo_dest = st.session_state.pop("demo_destination")
        st.session_state["prefill_destination"] = demo_dest

    # Top Navbar Header
    render_header()

    # Main Navigation Routing
    page = get_state("current_page", "Home")

    if page == "Home":
        render_hero(on_plan_click=lambda: set_state("current_page", "Plan Trip"))

    elif page == "Plan Trip":
        render_planner_and_results()

def render_planner_and_results():
    st.markdown("## ✈️ Plan Your Trip")
    st.markdown("Customize your travel parameters to generate an intelligent, personalized day-wise itinerary.")

    # Form Pre-fill values
    prefill = st.session_state.get("prefill_destination", "Hampi")

    # Planning Form Container
    with st.form("trip_planner_form"):
        col1, col2 = st.columns(2)

        with col1:
            destination = st.text_input(
                "📍 Destination Name",
                value=prefill,
                placeholder="e.g. Hampi, Jaipur, Varanasi, Agra, Rome, Paris",
                help="Enter any city, heritage site, or region."
            )
            duration = st.slider(
                "⏱️ Trip Duration (Days)",
                min_value=1,
                max_value=14,
                value=3,
                step=1
            )
            mood = st.selectbox(
                "🎭 Travel Mood",
                options=["Relaxed", "Adventurous", "Romantic", "Peaceful", "Cultural", "Spiritual", "Family", "Nature"],
                index=0,
                help="Your selected mood directly influences place recommendations."
            )

        with col2:
            travel_style = st.selectbox(
                "👥 Travel Style",
                options=["Solo", "Couple", "Family", "Friends"],
                index=0
            )
            budget = st.select_slider(
                "💰 Budget Level",
                options=["Budget", "Moderate", "Luxury"],
                value="Moderate"
            )
            interests = st.multiselect(
                "🎯 Primary Interests",
                options=["Heritage", "Nature", "Food", "Adventure", "Photography", "Temples", "Museums", "Shopping", "Local Culture"],
                default=["Heritage", "Nature", "Food"]
            )

        submit_btn = st.form_submit_button("✨ GENERATE TRIP ITINERARY", use_container_width=True)

    # Handle Form Submission
    if submit_btn:
        clean_dest = sanitize_text(destination)
        is_valid, err_msg = validate_trip_inputs(clean_dest, duration, mood, travel_style, budget, interests)

        if not is_valid:
            st.error(f"⚠️ {err_msg}")
            return

        with st.spinner(f"🔍 Geocoding {clean_dest}, fetching weather, heritage sites & generating itinerary..."):
            clear_trip_state()

            # 1. Geocode
            geo_info = geocode_destination(clean_dest)
            if not geo_info:
                st.error(f"Could not locate destination '{clean_dest}'. Please check spelling and try again.")
                return

            lat, lon = geo_info["lat"], geo_info["lon"]

            # 2. Fetch Wikipedia Summary
            wiki_info = fetch_wikipedia_summary(clean_dest)

            # 3. Fetch Destination Photos
            images = fetch_destination_images(clean_dest, count=4)

            # 4. Fetch Weather Forecast
            weather_data = fetch_weather_forecast(lat, lon)

            # 5. Fetch POIs & Heritage Sites
            attractions, heritage_sites = get_destination_places(clean_dest, lat, lon, mood, interests)

            # Combine places for itinerary engine
            all_places = heritage_sites + attractions

            # 6. Generate Personalized Day-wise Itinerary
            itinerary_data = generate_personalized_itinerary(
                destination=clean_dest,
                duration=duration,
                mood=mood,
                travel_style=travel_style,
                budget=budget,
                interests=interests,
                all_places=all_places
            )

            # 7. Calculate Budget Estimate
            budget_data = calculate_budget_estimate(duration, budget, travel_style)

            # Store in Session State
            set_state("trip_inputs", {
                "destination": clean_dest,
                "duration": duration,
                "mood": mood,
                "travel_style": travel_style,
                "budget": budget,
                "interests": interests
            })
            set_state("destination_info", geo_info)
            set_state("wiki_info", wiki_info)
            set_state("images", images)
            set_state("weather_data", weather_data)
            set_state("heritage_data", heritage_sites)
            set_state("attractions_data", attractions)
            set_state("itinerary_data", itinerary_data)
            set_state("budget_data", budget_data)

            st.success(f"🎉 Trip itinerary successfully generated for {clean_dest.title()}!")

    # Display Dashboard if results exist
    itinerary_data = get_state("itinerary_data")
    if itinerary_data:
        render_results_dashboard()

def render_results_dashboard():
    st.markdown("---")
    dest_info = get_state("destination_info", {})
    dest_name = dest_info.get("name", "Destination")
    inputs = get_state("trip_inputs", {})

    # Quick Summary Chip Bar
    st.markdown(
        f"""
        <div style="background: #1e293b; padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; border: 1px solid rgba(255,255,255,0.08);">
            <span style="font-size: 1.1rem; font-weight: 700; color: #38bdf8;">📍 {dest_name.title()}</span>
            <span class="tg-badge tg-badge-primary">⏱️ {inputs.get('duration')} Days</span>
            <span class="tg-badge tg-badge-heritage">🎭 {inputs.get('mood')} Mood</span>
            <span class="tg-badge tg-badge-accent">👥 {inputs.get('travel_style')}</span>
            <span class="tg-badge tg-badge-primary">💰 {inputs.get('budget')} Budget</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Multi-tab Dashboard Navigation
    tab_overview, tab_itinerary, tab_map, tab_heritage, tab_weather, tab_budget, tab_ai, tab_download = st.tabs([
        "📌 Overview",
        "🗓️ Itinerary",
        "🗺️ Interactive Map",
        "🏛️ Heritage & Culture",
        "🌤️ Weather",
        "💰 Budget",
        "🤖 AI Assistant",
        "📄 Download PDF"
    ])

    with tab_overview:
        render_destination_overview(
            destination_info=dest_info,
            wiki_info=get_state("wiki_info", {}),
            images=get_state("images", [])
        )

    with tab_itinerary:
        render_itinerary_timeline(get_state("itinerary_data", []))

    with tab_map:
        render_interactive_map(dest_info, get_state("itinerary_data", []), get_state("heritage_data", []))

    with tab_heritage:
        render_heritage_section(get_state("heritage_data", []), dest_name)

    with tab_weather:
        render_weather_widget(get_state("weather_data", {}))

    with tab_budget:
        render_budget_section(get_state("budget_data", {}))

    with tab_ai:
        ai_context = {
            "destination": dest_name,
            "mood": inputs.get("mood"),
            "duration": inputs.get("duration"),
            "weather": get_state("weather_data"),
            "budget": get_state("budget_data"),
            "heritage": get_state("heritage_data"),
            "itinerary": get_state("itinerary_data")
        }
        render_chatbot(ai_context)

    with tab_download:
        render_pdf_download_tab(dest_name, inputs)

def render_interactive_map(dest_info: Dict[str, Any], itinerary: List[Dict[str, Any]], heritage: List[Dict[str, Any]]):
    st.markdown("### 🗺️ Interactive Destination Map")
    st.markdown("Explore markers for your day-wise itinerary activities and local heritage landmarks.")

    lat = dest_info.get("lat", 20.5937)
    lon = dest_info.get("lon", 78.9629)

    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenStreetMap")

    # Center marker
    folium.Marker(
        [lat, lon],
        popup=f"<b>{dest_info.get('name')} Center</b>",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # Itinerary markers
    colors = ["blue", "green", "purple", "orange", "darkred", "cadetblue"]
    for day in itinerary:
        d_num = day.get("day", 1)
        color = colors[(d_num - 1) % len(colors)]
        for slot in day.get("slots", []):
            s_lat = slot.get("lat")
            s_lon = slot.get("lon")
            if s_lat and s_lon:
                popup_html = f"""
                <div style="font-family: sans-serif;">
                    <b>Day {d_num}: {slot.get('place')}</b><br/>
                    <i>{slot.get('period')} ({slot.get('category')})</i><br/>
                    {slot.get('activity')}
                </div>
                """
                folium.Marker(
                    [s_lat, s_lon],
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=f"Day {d_num}: {slot.get('place')}",
                    icon=folium.Icon(color=color, icon="star")
                ).add_to(m)

    # Heritage markers
    for h in heritage:
        h_lat = h.get("lat")
        h_lon = h.get("lon")
        if h_lat and h_lon:
            popup_html = f"""
            <div style="font-family: sans-serif;">
                <b>🏛️ {h.get('name')}</b><br/>
                <i>{h.get('category')}</i><br/>
                {h.get('description')}
            </div>
            """
            folium.Marker(
                [h_lat, h_lon],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"Heritage: {h.get('name')}",
                icon=folium.Icon(color="amber" if hasattr(folium.Icon, 'amber') else "orange", icon="home")
            ).add_to(m)

    st_folium(m, width=1100, height=500)

def render_budget_section(budget_data: Dict[str, Any]):
    st.markdown("### 💰 Trip Budget Estimation")
    if not budget_data:
        st.info("No budget data calculated.")
        return

    est_total = budget_data.get("total_estimated", 0)
    breakdown = budget_data.get("breakdown", {})
    usd_total = est_total / 83.0

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(
            f"""
            <div class="tg-card" style="text-align: center; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);">
                <div style="font-size: 0.9rem; color: #94a3b8;">Estimated Total Cost</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #38bdf8; margin: 0.5rem 0;">
                    ₹{est_total:,.0f}
                </div>
                <div style="font-size: 0.9rem; color: #cbd5e1;">(~${usd_total:,.0f} USD)</div>
                <div style="font-size: 0.78rem; color: #64748b; margin-top: 0.6rem;">
                    Estimates based on {budget_data.get('budget_tier')} tier & {budget_data.get('travel_style')} style.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown("#### Expense Breakdown")
        for category, amt in breakdown.items():
            perc = (amt / est_total) * 100 if est_total > 0 else 0
            st.markdown(f"**{category}**: ₹{amt:,.0f} (*{perc:.0f}%*)")
            st.progress(min(1.0, perc / 100.0))

def render_pdf_download_tab(dest_name: str, inputs: Dict[str, Any]):
    st.markdown("### 📄 Export Complete Itinerary to PDF")
    st.markdown(
        """
        Download a professionally formatted offline PDF report containing your day-wise itinerary, 
        heritage discoveries, weather forecast, budget breakdown, and travel tips.
        """
        , unsafe_allow_html=True
    )

    pdf_bytes = generate_itinerary_pdf(
        destination=dest_name,
        trip_inputs=inputs,
        itinerary_data=get_state("itinerary_data", []),
        heritage_data=get_state("heritage_data", []),
        weather_data=get_state("weather_data", {}),
        budget_data=get_state("budget_data", {})
    )

    st.download_button(
        label="📥 DOWNLOAD PDF ITINERARY",
        data=pdf_bytes,
        file_name=f"TripGenie_{dest_name.title()}_Itinerary.pdf",
        mime="application/pdf",
        use_container_width=True
    )

if __name__ == "__main__":
    main()
