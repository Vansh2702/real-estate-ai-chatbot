import pandas as pd
import streamlit as st

# Load the Excel file
df = pd.read_excel("MIDC RATES.xlsx")

# Clean the data
df = df.dropna(subset=['Location'])
df[['District', 'Taluka']] = df[['District', 'Taluka']].ffill()

# Page setup
st.set_page_config(page_title="MIDC Land Rate Finder", layout="centered")
st.title("🏡 MIDC Land Rate Finder")
st.markdown("Select a district, taluka, location, and rate type to view rates.")

# Dropdown 1: District
districts = sorted(df['District'].unique().tolist())
selected_district = st.selectbox("📍 Select District", districts)

# Dropdown 2: Taluka (filtered)
talukas = sorted(df[df['District'] == selected_district]['Taluka'].unique().tolist())
selected_taluka = st.selectbox("🗺️ Select Taluka", talukas)

# Dropdown 3: Location (filtered)
locations = sorted(df[(df['District'] == selected_district) & (df['Taluka'] == selected_taluka)]['Location'].unique().tolist())
selected_location = st.selectbox("📌 Select Location", locations)

# Dropdown 4: Rate Type
rate_types = ["Industrial Rate", "Residential Rate", "Commercial Rate"]
selected_rate_type = st.selectbox("💼 Select Rate Type", rate_types)

# Show Rate Button
if st.button("💰 Show Rate"):
    row = df[
        (df['District'] == selected_district) &
        (df['Taluka'] == selected_taluka) &
        (df['Location'] == selected_location)
    ]
    if row.empty:
        st.warning("No rate found for this selection.")
    else:
        rate = row.iloc[0][selected_rate_type]
        if pd.isna(rate) or str(rate).strip().lower() == "not applicable":
            st.error("Rate not available for this selection.")
        else:
            st.success(f"{selected_rate_type} in {selected_location}, {selected_taluka}, {selected_district} is **{rate}**")
