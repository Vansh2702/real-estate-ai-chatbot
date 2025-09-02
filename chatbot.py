import streamlit as st
import pandas as pd

# --- Load and clean the data ---
df = pd.read_excel("MIDC RATES.xlsx")
df = df.dropna(subset=['Location'])
df[['District', 'Taluka']] = df[['District', 'Taluka']].ffill()

# Create lowercase location map for fast matching
location_map = {
    str(row['Location']).lower(): (row['District'], row['Taluka'], row['Location'])
    for _, row in df.iterrows()
}

# --- Match user input to location, taluka, or district ---
def match_location(user_input):
    user_input = user_input.lower().strip()

    # Exact location match
    if user_input in location_map:
        return location_map[user_input]

    # Partial location match
    for loc in location_map:
        if user_input in loc:
            return location_map[loc]

    # Taluka match
    taluka_matches = df[df['Taluka'].str.lower() == user_input]
    if not taluka_matches.empty:
        row = taluka_matches[taluka_matches['Location'].str.lower() == user_input]
        row = row.iloc[0] if not row.empty else taluka_matches.iloc[0]
        return (row['District'], row['Taluka'], row['Location'])

    # District match
    district_matches = df[df['District'].str.lower() == user_input]
    if not district_matches.empty:
        row = district_matches[district_matches['Location'].str.lower() == user_input]
        row = row.iloc[0] if not row.empty else district_matches.iloc[0]
        return (row['District'], row['Taluka'], row['Location'])

    return None

# --- Get rate for a location and rate type ---
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

# --- Streamlit Setup ---
st.set_page_config("🏡 MIDC Property Rate Chatbot", layout="centered")
st.title("🏡 MIDC Property Rate Chatbot")

# --- Session State Setup ---
if "chat" not in st.session_state:
    st.session_state.chat = []
if "location" not in st.session_state:
    st.session_state.location = None
if "rate_type" not in st.session_state:
    st.session_state.rate_type = None
if "new_input" not in st.session_state:
    st.session_state.new_input = None

# --- Start New Chat ---
if st.button("🆕 Start New Chat"):
    st.session_state.chat = []
    st.session_state.location = None
    st.session_state.rate_type = None
    st.session_state.new_input = None
    st.rerun()

# --- Show Chat History (Chat Bubbles) ---
for msg in st.session_state.chat:
    is_user = msg["role"] == "user"
    bubble_style = """
        background-color: {bg};
        color: #1b1e21;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 75%;
        float: {align};
        clear: both;
        font-weight: bold;
        text-align: {text_align};
    """.format(
        bg="#d4edda" if is_user else "#ffffff",
        align="right" if is_user else "left",
        text_align="right" if is_user else "left"
    )
    st.markdown(
        f"<div style='{bubble_style}'>{'You' if is_user else '🏠 Bot'}: {msg['content']}</div>",
        unsafe_allow_html=True
    )

# --- Handle Chat Input ---
user_input = st.chat_input("Ask about MIDC property rates...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    st.session_state.new_input = user_input
    st.rerun()

# --- Process Input After Rerun ---
if st.session_state.new_input:
    user_input = st.session_state.new_input.strip()
    st.session_state.new_input = None  # Clear it

    response = ""

    # STEP 1: Location
    if st.session_state.location is None and st.session_state.rate_type is None:
        location = match_location(user_input)
        if location:
            st.session_state.location = location
            response = "📍 Got it! What type of property are you interested in – Industrial, Commercial, or Residential?"
        elif user_input.lower() in ["industrial", "residential", "commercial"]:
            response = "❗ Please tell me where you'd like to buy the property first."
        else:
            response = "🏠 Please provide a valid location, taluka, or district."

    # STEP 2: Rate Type
    elif st.session_state.location and st.session_state.rate_type is None:
        type_map = {
            "industrial": "Industrial Rate",
            "residential": "Residential Rate",
            "commercial": "Commercial Rate"
        }
        selected = next((v for k, v in type_map.items() if k in user_input.lower()), None)

        if selected:
            st.session_state.rate_type = selected
            d, t, l = st.session_state.location
            rate = get_rate(d, t, l, selected)
            if rate:
                response = f"💰 The **{selected}** in **{l}, {t}, {d}** is **{rate}**."
            else:
                response = f"❌ No {selected} available in {l}, {t}, {d}."
        else:
            response = "🏷️ Please choose: Industrial, Commercial, or Residential."

    # STEP 3: Finish & Reset
    else:
        st.session_state.location = None
        st.session_state.rate_type = None
        response = "✅ Would you like to check another property rate?"

    st.session_state.chat.append({"role": "assistant", "content": response})
    st.rerun()
