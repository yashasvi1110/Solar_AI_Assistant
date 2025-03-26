import streamlit as st  # type: ignore
import requests
import json
import os
import re
from dotenv import load_dotenv  # type: ignore

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("API Key is missing! Set OPENROUTER_API_KEY in a .env file.")
    st.stop()

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "your_site_url",
    "X-Title": "your_site_name",
}

def get_solar_advice(query):
    """Fetch AI response using OpenRouter with Gemini Flash Lite 2.0 Preview (free)."""
    data = {
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
        "messages": [
            {"role": "system", "content": "You are a solar energy expert AI."},
            {"role": "user", "content": query},
        ],
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=HEADERS,
        data=json.dumps(data),
    )

    try:
        json_response = response.json()
        return json_response["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return f"Error: Unexpected response format: {response.text}"


def is_solar_related(question):
    """
    Validates if the question is solar energy-related.
    Returns True if the question contains relevant keywords, False otherwise.
    """
    solar_keywords = [
        "solar energy", "solar panel", "solar power", "photovoltaic",
        "renewable energy", "solar system", "solar installation",
        "solar efficiency", "solar battery", "solar inverter", "solar", "photovoltaic", "PV", "sunlight", "solar panel", "renewable energy", "inverter", "battery storage", "LCOE", "grid-tied", "off-grid", "solar efficiency", "net metering", "solar installation","solar energy", "solar power", "photovoltaics", "solar panels", "solar cells",
    "renewable energy", "solar radiation", "solar efficiency", "solar thermal",
    "solar inverter", "solar battery", "solar storage", "solar array", "net metering",
    "solar farms", "solar grid", "solar tracking", "off-grid solar", "grid-tied solar",
    "solar rooftop", "solar heating", "solar cooling", "solar water heater",
    "solar concentrator", "solar thermal collector", "solar photovoltaic (PV)",
    "solar energy conversion", "solar hybrid system", "solar electrification",
    "solar charge controller", "solar module", "monocrystalline solar panel",
    "polycrystalline solar panel", "thin-film solar panel", "solar LED lighting",
    "solar economics", "solar subsidies", "solar policy", "solar installation",
    "solar maintenance", "solar degradation", "solar power plant", "floating solar",
    "solar carport", "solar-powered devices", "solar energy storage",
    "solar energy advantages", "solar energy disadvantages", "solar industry",
    "solar research", "solar grid integration", "solar innovation","energy"
    ]
    pattern = r"\b(" + "|".join(solar_keywords) + r")\b"
    return bool(re.search(pattern, question, re.IGNORECASE))


# Custom CSS for the button
st.markdown("""
    <style>
    .combined-button {
        background: linear-gradient(90deg, #f39c12, #f1c40f); /* Orange to yellow gradient */
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease; /* Smooth transition for all properties */
        opacity: 1; /* Fully visible initially */
        box-shadow: none; /* No shadow initially */
    }
    .combined-button:hover {
        opacity: 0.9; /* Slight transparency on hover */
        transform: scale(1.1); /* Button grows slightly */
        background: linear-gradient(90deg, #e67e22, #f39c12); /* Darker gradient on hover */
        box-shadow: 0px 8px 20px rgba(243, 156, 18, 0.5); /* Glow effect */
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("☀️ Solar AI Assistant")
st.write("💡Illuminate your solar journey with expert insights!")

# Input Box
user_input = st.text_input("Ask me anything about solar energy...")

# Search Button
search_button = st.markdown(
    '<button class="combined-button">🔍Get Answer</button>', unsafe_allow_html=True
)

if user_input:
    if is_solar_related(user_input):
        # Fetch and display the answer if the question is valid
        answer = get_solar_advice(user_input)
        st.write("### ✨Answer:")
        st.write(answer)
    else:
        # Warn the user if the question is not solar energy-related
        st.warning("I'm specialized in solar energy topics. Please ask something related to solar technology, installation, market trends or its related aspects!")
