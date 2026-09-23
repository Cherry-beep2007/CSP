# TRIPGENIE ✈️
### *Smart Gateway to Your Destination*
**A Community Service Project focused on Tourism & Local Heritage Discovery**

---

## 🌟 1. Project Overview & Problem Statement
Many travelers, tourists, and heritage enthusiasts remain unaware of the rich attractions, historic monuments, temples, forts, and cultural experiences available in and around destinations. Most travel tools rely on rigid generic lists or paid commercial sponsors, overlooking local heritage and personalized traveler needs.

**TripGenie** solves this problem by providing an intelligent, personalized travel-planning platform. Based on destination, trip duration, traveler mood, travel style, interests, and budget, TripGenie generates:
- An optimized **day-wise itinerary** (Morning, Afternoon, Evening).
- A dedicated **Local Heritage & Culture discovery module**.
- **Real destination imagery** & Wikipedia background.
- **7-day weather forecasts & rain-aware travel tips** from Open-Meteo.
- An **Interactive Map** with place sequence markers.
- A **Context-Aware AI Travel Assistant**.
- A downloadable **Offline PDF Itinerary Report**.

---

## 🏗️ 2. System Architecture
TripGenie is designed following clean, modular software engineering practices:

```
tripgenie/
│
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Project dependencies
├── .env.example                # Template for environment variables
├── .gitignore                  # Git exclusion rules
├── README.md                   # Comprehensive project documentation
│
├── services/                   # Modular API and business logic services
│   ├── geocoding_service.py    # OpenStreetMap Nominatim geocoding & fallback
│   ├── wikipedia_service.py    # Wikipedia summary & page metadata API
│   ├── image_service.py        # Unsplash API client & curated fallback photo bank
│   ├── weather_service.py      # Open-Meteo 7-day weather API & rain alerts
│   ├── places_service.py       # Overpass API (OSM) & heritage POI discovery
│   ├── itinerary_service.py   # Day-wise itinerary generator & budget estimator
│   └── ai_service.py           # Modular LLM Assistant (Gemini/OpenAI/Rule-based)
│
├── components/                 # Reusable UI components & custom styling
│   ├── styles.py               # Custom CSS design system injection
│   ├── header.py               # Navbar & branding header
│   ├── hero.py                 # Hero section & Community Project landing
│   ├── destination_card.py     # Destination overview & photo gallery
│   ├── itinerary_card.py       # Timeline cards for day-by-day activities
│   ├── heritage_card.py        # Dedicated heritage monument cards
│   ├── weather_card.py         # Weather widget & 5-day forecast cards
│   └── chatbot.py              # Interactive AI travel assistant UI
│
├── utils/                      # Helper & utility functions
│   ├── cache.py                # Streamlit session state management & clear routines
│   ├── validators.py           # Input validation & text sanitization
│   ├── route_optimizer.py      # Haversine distance calculation & nearest-neighbor route optimizer
│   └── pdf_generator.py        # ReportLab PDF document export generator
│
└── data/
    └── heritage_data.json      # Curated pre-seeded heritage database for major destinations
```

---

## 🛠️ 3. Technology Stack & API Integrations

| Layer | Technology / Service | Description |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit + Custom CSS | Glassmorphism design, custom fonts (Plus Jakarta Sans), responsive tabs, custom timeline cards |
| **Language** | Python 3.11+ | Backend application logic and service layer |
| **Data & Routing** | Pandas, Math, Haversine | Distance estimation and route optimization |
| **Geocoding** | OpenStreetMap Nominatim API | Latitude/Longitude, bounding box, and location lookup |
| **Heritage & POIs** | OSM Overpass API + Heritage JSON | Live historic monument query and offline database matching |
| **Destination Data** | Wikipedia REST API | Comprehensive historical summary & article links |
| **Imagery** | Unsplash API / Wikimedia | High-resolution destination & attraction photography |
| **Weather** | Open-Meteo API | Free 7-day weather forecast, precipitation probability, weather codes |
| **Interactive Map**| Folium & streamlit-folium | Interactive map with color-coded day markers & heritage pins |
| **PDF Export** | ReportLab | Production PDF generation for offline travel use |
| **AI Assistant** | Google Gemini / OpenAI / Rule AI | Contextual travel assistant answering user queries |

---

## 🚀 4. Installation & Quick Start

### Prerequisites
- Python 3.11+ installed on your system.
- `pip` package manager.

### Step 1: Clone or Navigate to Directory
```bash
cd C:\Users\Charitha\.gemini\antigravity-ide\scratch\tripgenie
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Optionally add your API keys:
- `UNSPLASH_ACCESS_KEY` (Optional for Unsplash photo API)
- `GEMINI_API_KEY` or `OPENAI_API_KEY` (Optional for LLM chatbot; intelligent rule-based fallback assistant works out-of-the-box!)

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 🎭 5. Mood-Based Recommendation Logic
TripGenie adapts place recommendations based on user mood:
- **RELAXED:** Prioritizes lakes, gardens, riverfront strolls, cafes, and leisurely sights.
- **ADVENTUROUS:** Prioritizes hilltop fortresses, trekking trails, viewpoints, and outdoor exploration.
- **ROMANTIC:** Prioritizes sunset spots, palace courtyards, scenic viewpoints, and cozy quarters.
- **PEACEFUL:** Prioritizes quiet temples, spiritual shrines, monastic gardens, and serene waters.
- **CULTURAL:** Prioritizes ancient monuments, museums, heritage corridors, and traditional markets.
- **FAMILY / NATURE / SPIRITUAL:** Tailors categories specifically to family accessibility or nature trails.

---

## 🛡️ 6. Error Handling & Caching Strategy
- **API Resilience:** Every external API request (Nominatim, Overpass, Wikipedia, Open-Meteo, Unsplash) includes explicit timeouts, headers, safe JSON parsing, and graceful fallbacks.
- **Offline Data Fallback:** If network connection or Overpass API times out, TripGenie relies on `heritage_data.json` and synthetic coordinate generation so the app **never crashes**.
- **Caching:** `@st.cache_data` is used for geocoding, weather forecasts, Wikipedia summaries, and image searches to minimize API calls and keep execution instantaneous.

---

## 📄 7. PDF Export Feature
Clicking **DOWNLOAD PDF ITINERARY** in the Download tab triggers `utils/pdf_generator.py` to compile a report containing:
- Document header & TripGenie branding.
- Destination summary & trip parameters.
- Day-wise timeline table with times, places, activities, and distance estimates.
- Heritage & Cultural Site highlights.
- Trip Budget breakdown table.
- Timestamp & Community Project footer.

---

## 📜 8. Community Service Alignment
This project directly fulfills community service objectives by:
1. Promoting awareness of lesser-known local heritage monuments and historic shrines.
2. Offering a free, accessible, and ad-free travel planning software tool.
3. Enabling offline itinerary access via downloadable PDFs for travelers with limited connectivity.

---

## 🔮 9. Future Enhancements
- Support for multi-destination road trip itineraries.
- Audio guide integration for heritage sites using Text-to-Speech (TTS).
- Integration with local public transit routes and real-time train schedules.
