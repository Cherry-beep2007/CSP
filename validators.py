import re
from typing import Tuple, Dict, Any, List

def validate_trip_inputs(
    destination: str,
    duration: int,
    mood: str,
    travel_style: str,
    budget: str,
    interests: List[str]
) -> Tuple[bool, str]:
    """
    Validates user input for trip planning.
    Returns (is_valid, error_message).
    """
    if not destination or not destination.strip():
        return False, "Destination name cannot be empty."

    clean_dest = destination.strip()
    if len(clean_dest) < 2:
        return False, "Destination name must be at least 2 characters long."

    if re.search(r'[<>{}\[\]\\]', clean_dest):
        return False, "Destination contains invalid special characters."

    if duration < 1 or duration > 30:
        return False, "Trip duration must be between 1 and 30 days."

    valid_moods = [
        "Relaxed", "Adventurous", "Romantic", "Peaceful",
        "Cultural", "Spiritual", "Family", "Nature"
    ]
    if mood not in valid_moods:
        return False, f"Please select a valid mood from: {', '.join(valid_moods)}"

    valid_styles = ["Solo", "Couple", "Family", "Friends"]
    if travel_style not in valid_styles:
        return False, f"Please select a valid travel style from: {', '.join(valid_styles)}"

    valid_budgets = ["Budget", "Moderate", "Luxury"]
    if budget not in valid_budgets:
        return False, f"Please select a valid budget level."

    if not interests or len(interests) == 0:
        return False, "Please select at least one interest to tailor your trip."

    return True, ""

def sanitize_text(text: str) -> str:
    """Sanitizes user query or string inputs for display/AI prompts."""
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]*>', '', text)
    return clean.strip()
