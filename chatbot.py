import streamlit as st
import pandas as pd

# --- Load and clean Excel data ---
df = pd.read_excel("MIDC RATES.xlsx")
df = df.dropna(subset=['Location'])
df[['District', 'Taluka']] = df[['District', 'Taluka']].ffill()

# Build a lowercase location map from the "Location" column
location_map = {
    str(row['Location']).lower(): (row['District'], row['Taluka'], row['Location'])
    for _, row in df.iterrows()
}

# --- Function to find location from user input ---
def match_location(user_input):
    user_input = user_input.lower().strip()

    # Match from Location column
    for loc in location_map:
        if user_input in loc or loc in user_input:
            return location_map[loc]

    # Match from Taluka
    matches = df[df['Taluka'].str.lower() == user_input]
    if not matches.empty:
        row = matches.iloc[0]
        return (row['District'], row['Taluka'], row['Location'])

    # Match from District
    matches = df[df['District'].str.lower() == user_input]
    if not matches.empty:
        row = matches.iloc[0]
        return (row['District'], row['Taluka'], row['Location'])

    return None

# --- Get rate from Excel ---
def get_rate(district, taluka, location, rate_type):
    row = df[
        (df['District'] == district) &
        (df['Taluka'] == taluka) &
        (df['Location'] == location)
    ]
    if row.empty:
        return None
    rate = row.iloc[0][rate_type]
    return rate if pd.notna(rate) else None

# --- Page Config ---
st.set_page_config("🏡 MIDC Property Rate Assistant", layout="centered")
st.title("🏡 MIDC Property Rate Chatbot")

# --- Session State Initialization ---
if "chat" not in st.session_state:
    st.session_state.chat = []
if "location" not in st.session_state:
    st.session_state.location = None
if "rate_type" not in st.session_state:
    st.session_state.rate_type = None

# --- Reset Button ---
if st.button("🆕 Start New Chat"):
    st.session_state.chat = []
    st.session_state.location = None
    st.session_state.rate_type = None
    st.rerun()

# --- Display Chat Bubbles (Dark Mode Compatible) ---
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style='
                background-color: #d4edda;
                color: #1b1e21;
                padding: 10px 15px;
                border-radius: 10px;
                margin: 5px 0;
                max-width: 75%;
                float: right;
                clear: both;
                font-weight: bold;
                text-align: right;
            '>
                You: {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='
                background-color: #ffffff;
                color: #1b1e21;
                padding: 10px 15px;
                border-radius: 10px;
                margin: 5px 0;
                max-width: 75%;
                float: left;
                clear: both;
                font-weight: bold;
                text-align: left;
            '>
                🏠 Bot: {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Chat Input Box ---
user_input = st.chat_input("Ask about MIDC property rates...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    response = ""

    # STEP 1: Ask for location
    if st.session_state.location is None:
        matched_location = match_location(user_input)
        if matched_location:
            st.session_state.location = matched_location
            response = "📍 Got it! What type of property are you interested in – Industrial, Commercial, or Residential?"
        else:
            response = "🏠 Sure! Where do you want to buy property? Please provide a valid location, taluka, or district."

    # STEP 2: Ask for property type
    elif st.session_state.rate_type is None:
        type_map = {
            "industrial": "Industrial Rate",
            "residential": "Residential Rate",
            "commercial": "Commercial Rate"
        }
        found = None
        for word, rate_label in type_map.items():
            if word in user_input.lower():
                found = rate_label
                break
        if found:
            st.session_state.rate_type = found
            district, taluka, location = st.session_state.location
            rate = get_rate(district, taluka, location, found)
            if rate:
                response = f"💰 The **{found}** in **{location}, {taluka}, {district}** is **{rate}**."
            else:
                response = f"❌ No {found} available in {location}, {taluka}, {district}."
        else:
            response = "🏷️ Please specify the type: Industrial, Commercial, or Residential."

    # STEP 3: Done, reset for next query
    else:
        st.session_state.location = None
        st.session_state.rate_type = None
        response = "✅ Would you like to check another property rate?"

    st.session_state.chat.append({"role": "assistant", "content": response})
