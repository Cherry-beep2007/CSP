import os
import requests
from typing import Dict, Any, List

def query_ai_assistant(
    user_prompt: str,
    context: Dict[str, Any],
    chat_history: List[Dict[str, str]]
) -> str:
    """
    Modular AI assistant dispatcher supporting Gemini, OpenAI, or intelligent rule-based fallback.
    Injects destination, itinerary, weather, mood, budget, and heritage context.
    """
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()

    dest = context.get("destination", "Destination")
    mood = context.get("mood", "Relaxed")
    duration = context.get("duration", 1)
    weather = context.get("weather", {})
    budget = context.get("budget", {})
    heritage = context.get("heritage", [])
    itinerary = context.get("itinerary", [])

    system_context = f"""
    You are TripGenie AI Assistant, a warm, knowledgeable local travel expert and heritage curator for {dest}.
    Current Trip Context:
    - Destination: {dest}
    - Mood: {mood}
    - Duration: {duration} Days
    - Budget Tier: {budget.get('budget_tier', 'Moderate')} (Est Total: ₹{budget.get('total_estimated', 0):,.0f})
    - Weather Condition: {weather.get('current_condition', 'Pleasant')}, {weather.get('current_temp', 25)}°C. Rain alert: {weather.get('rain_alert', False)}
    - Key Heritage Sites: {', '.join([h['name'] for h in heritage[:4]]) if heritage else 'Local historic landmarks'}
    
    Instruction: Answer concisely, with clear travel recommendations and enthusiastic heritage knowledge.
    """

    # Try Gemini API if key provided
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            full_prompt = f"{system_context}\n\nUser Question: {user_prompt}"
            response = model.generate_content(full_prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")

    # Try OpenAI API if key provided
    if openai_key:
        try:
            headers = {
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 400
            }
            resp = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenAI API error: {e}")

    # Intelligent Rule-Based Fallback Assistant
    return generate_rule_based_ai_response(user_prompt, context)

def generate_rule_based_ai_response(prompt: str, context: Dict[str, Any]) -> str:
    """Intelligent offline fallback bot providing tailored responses based on trip context."""
    p_lower = prompt.lower()
    dest = context.get("destination", "your destination").title()
    mood = context.get("mood", "Relaxed")
    weather = context.get("weather", {})
    budget = context.get("budget", {})
    heritage = context.get("heritage", [])
    itinerary = context.get("itinerary", [])

    if "rain" in p_lower or "weather" in p_lower:
        if weather.get("rain_alert"):
            return f"☔ **Rainy Day Travel Tip for {dest}:**\nSince rain is expected, TripGenie recommends visiting indoor heritage locations! Top picks include the local Museums, covered Palaces, and indoor art galleries. Don't forget an umbrella and comfortable waterproof shoes!"
        else:
            return f"☀️ **Weather Outlook for {dest}:**\nThe current weather is {weather.get('current_condition', 'Pleasant')} at {weather.get('current_temp', 25)}°C. Perfect for outdoor heritage monuments, garden strolls, and scenic viewpoints!"

    elif "pack" in p_lower or "clothing" in p_lower or "what to bring" in p_lower:
        return f"🎒 **Packing Guide for {dest} ({mood} Trip):**\n" \
               f"1. **Attire:** Comfortable cotton/breathable clothing for daytime walking, plus a light jacket for cool evenings.\n" \
               f"2. **Footwear:** Broken-in walking shoes or sturdy sandals for exploring heritage stone paving and monument stairs.\n" \
               f"3. **Essentials:** Reusable water bottle, sun protection (hat/sunglasses/sunscreen), power bank, and a compact umbrella.\n" \
               f"4. **Cultural respect:** Modest clothing covering shoulders and knees when visiting active places of worship."

    elif "budget" in p_lower or "cheap" in p_lower or "money" in p_lower or "save" in p_lower:
        total = budget.get("total_estimated", 0)
        return f"💰 **Budget Optimization Tips for {dest}:**\n" \
               f"Your estimated trip budget is **₹{total:,.0f}**. Here is how to save:\n" \
               f"• **Transport:** Use local auto-rickshaws, public transit, or walkable routes instead of private cabs.\n" \
               f"• **Dining:** Enjoy authentic heritage street food and local thalis at busy family restaurants.\n" \
               f"• **Entry Tickets:** Look for combined heritage monuments passes or student/senior discount rates!"

    elif "heritage" in p_lower or "history" in p_lower or "site" in p_lower:
        if heritage:
            top_h = heritage[0]
            return f"🏛️ **Must-Visit Heritage Landmark in {dest}:**\n" \
                   f"Don't miss **{top_h.get('name')}** ({top_h.get('category')})!\n\n" \
                   f"*{top_h.get('description')}*\n\n" \
                   f"**Cultural Significance:** {top_h.get('cultural_relevance')}"
        else:
            return f"🏛️ **Heritage Discovery in {dest}:**\n{dest} is rich in historical heritage. Be sure to visit the central fort, ancient temple corridors, and old town bazaars."

    elif "modify" in p_lower or "change" in p_lower or "day 2" in p_lower or "day 1" in p_lower:
        return f"✨ **Itinerary Customization:**\nTo modify any day in your itinerary, you can swap afternoon outdoor spots with indoor heritage museums or adjust your trip mood in the planner tab! If you need specific venue recommendations for Day 2, check the Local Heritage tab for top-rated spots."

    elif "tomorrow" in p_lower or "next" in p_lower:
        if len(itinerary) > 1:
            d2 = itinerary[1]
            slots = d2.get("slots", [])
            places_list = ", ".join([s['place'] for s in slots])
            return f"🗓️ **Tomorrow's Recommended Plan (Day 2: {d2.get('theme')}):**\n" \
                   f"Your itinerary includes: **{places_list}**.\n" \
                   f"Start early in the morning to beat crowds at the first monument!"

    # Generic contextual response
    return f"🤖 **TripGenie Travel Assistant:**\n" \
           f"Glad to help with your trip to **{dest}**! Your trip is set for a **{mood}** travel style over **{len(itinerary)} days**. " \
           f"You can ask me about packing tips, weather updates, budget savings, or heritage site highlights!"
