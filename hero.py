import streamlit as st

def render_hero(on_plan_click):
    """Renders the high-impact landing page hero and feature grid."""
    st.markdown(
        """
        <div class="tg-hero-card">
            <span class="tg-badge tg-badge-heritage">COMMUNITY SERVICE TOURISM PROJECT</span>
            <div class="tg-hero-title">Your AI-Powered Gateway to Unforgettable Journeys</div>
            <div class="tg-hero-sub">
                Discover destinations, heritage monuments, attractions, and personalized travel experiences 
                tailored to your mood, schedule, budget, and travel style.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Primary Action Buttons
    col_cta1, col_cta2, col_space = st.columns([1.5, 1.5, 3])
    with col_cta1:
        if st.button("🚀 PLAN MY TRIP", key="hero_plan_cta", use_container_width=True):
            st.session_state["current_page"] = "Plan Trip"
            st.rerun()
    with col_cta2:
        if st.button("🏛️ EXPLORE HERITAGE", key="hero_explore_cta", use_container_width=True):
            # Pre-load Hampi demo trip
            st.session_state["demo_destination"] = "Hampi"
            st.session_state["current_page"] = "Plan Trip"
            st.rerun()

    st.markdown("---")

    # Feature Grid
    st.markdown("### 🌟 Why TripGenie?")
    
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(
            """
            <div class="tg-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
                <h4 style="margin: 0; color: #f8fafc;">Mood Recommendation</h4>
                <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.5rem;">
                    Personalized itineraries that adapt whether you want a relaxed, adventurous, romantic, or peaceful journey.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f2:
        st.markdown(
            """
            <div class="tg-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏛️</div>
                <h4 style="margin: 0; color: #f8fafc;">Heritage & Culture</h4>
                <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.5rem;">
                    Uncover historical monuments, temples, forts, and local culture to promote accessible heritage tourism.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f3:
        st.markdown(
            """
            <div class="tg-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌤️</div>
                <h4 style="margin: 0; color: #f8fafc;">Weather Insights</h4>
                <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.5rem;">
                    Live 7-day weather forecasts from Open-Meteo with smart rain warnings and indoor alternatives.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f4:
        st.markdown(
            """
            <div class="tg-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📄</div>
                <h4 style="margin: 0; color: #f8fafc;">Offline PDF Export</h4>
                <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.5rem;">
                    Download complete day-wise trip reports generated via ReportLab for seamless offline travel access.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Community Project Context Banner
    st.markdown(
        """
        <div class="tg-card" style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.9)); border-left: 4px solid #fbbf24;">
            <h4 style="margin-top: 0; color: #fbbf24;">ℹ️ Community Service Tourism Objective</h4>
            <p style="font-size: 0.9rem; color: #cbd5e1; margin: 0;">
                Many travellers remain unaware of significant heritage sites, local monuments, and cultural experiences surrounding famous destinations. 
                TripGenie bridges this gap by automatically discovering nearby historical landmarks, empowering local cultural preservation, 
                and delivering personalized itineraries free of charge.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
