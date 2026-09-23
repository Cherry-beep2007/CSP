import streamlit as st


def init_session_state():
    defaults = {
        "current_page": "Home",
        "trip_inputs": {},
        "destination_info": {},
        "wiki_info": {},
        "images": [],
        "weather_data": {},
        "heritage_data": [],
        "attractions_data": [],
        "itinerary_data": [],
        "budget_data": {},
        "chat_messages": [],
        "prefill_destination": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_state(key, default=None):
    return st.session_state.get(key, default)


def set_state(key, value):
    st.session_state[key] = value


def clear_trip_state():
    keys = [
        "trip_inputs",
        "destination_info",
        "wiki_info",
        "images",
        "weather_data",
        "heritage_data",
        "attractions_data",
        "itinerary_data",
        "budget_data",
        "chat_messages",
    ]

    for key in keys:
        st.session_state.pop(key, None)