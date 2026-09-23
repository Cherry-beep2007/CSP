import streamlit as st

def render_header():
    """Renders the top navigation bar and logo branding."""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(
            """
            <div class="tg-navbar">
                <div>
                    <div class="tg-brand">✈️ TRIPGENIE</div>
                    <div class="tg-tagline">Smart Gateway to Your Destination &bull; Community Heritage Initiative</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # Navigation Quick Actions
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏠 Home", key="nav_home_btn", use_container_width=True):
                st.session_state["current_page"] = "Home"
                st.rerun()
        with c2:
            if st.button("🗺️ Plan Trip", key="nav_plan_btn", use_container_width=True):
                st.session_state["current_page"] = "Plan Trip"
                st.rerun()
