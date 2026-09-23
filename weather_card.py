import streamlit as st
from typing import Dict, Any

def render_weather_widget(weather_data: Dict[str, Any]):
    """Renders weather forecast cards and custom travel advice."""
    if not weather_data:
        st.info("Weather data currently unavailable.")
        return

    st.markdown("### 🌤️ Live Weather Insights & Travel Advice")

    curr_temp = weather_data.get("current_temp", 24)
    curr_cond = weather_data.get("current_condition", "Partly Cloudy")
    curr_icon = weather_data.get("current_icon", "⛅")
    travel_tip = weather_data.get("travel_tip", "")
    rain_alert = weather_data.get("rain_alert", False)
    forecast = weather_data.get("daily_forecast", [])

    # Main Weather Status Box
    alert_border = "#ef4444" if rain_alert else "#38bdf8"
    st.markdown(
        f"""
        <div class="tg-weather-box" style="border-left: 5px solid {alert_border};">
            <div style="font-size: 3rem;">{curr_icon}</div>
            <div style="flex-grow: 1;">
                <div style="font-size: 1.8rem; font-weight: 700; color: #f8fafc;">
                    {curr_temp}°C <span style="font-size: 1rem; color: #94a3b8; font-weight: 400;">({curr_cond})</span>
                </div>
                <div style="font-size: 0.9rem; color: #cbd5e1; margin-top: 0.3rem;">
                    💡 <b>TripGenie Weather Advisory:</b> {travel_tip}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Multi-day Forecast Grid
    if forecast:
        st.markdown("#### 📅 Multi-Day Weather Forecast")
        f_cols = st.columns(min(len(forecast), 5))
        for idx, day in enumerate(forecast[:5]):
            with f_cols[idx]:
                st.markdown(
                    f"""
                    <div class="tg-card" style="text-align: center; padding: 1rem 0.5rem;">
                        <div style="font-size: 0.8rem; color: #94a3b8;">{day.get('date', f'Day {idx+1}')}</div>
                        <div style="font-size: 2rem; margin: 0.4rem 0;">{day.get('icon', '⛅')}</div>
                        <div style="font-weight: 700; color: #f8fafc; font-size: 1rem;">
                            {day.get('max_temp')}° / <span style="color: #94a3b8;">{day.get('min_temp')}°</span>
                        </div>
                        <div style="font-size: 0.75rem; color: #38bdf8; margin-top: 0.3rem;">
                            ☔ {day.get('precip_prob', 0)}% Rain
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
