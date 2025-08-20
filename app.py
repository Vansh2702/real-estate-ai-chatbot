import pandas as pd

# === Load the Excel ===
file_path = "MIDC RATES.xlsx"
df = pd.read_excel(file_path)

# === Clean the data ===
df = df.dropna(subset=['Location'])  # drop if location is missing
df[['District', 'Taluka']] = df[['District', 'Taluka']].ffill()

# === Helper Functions ===
def get_all_districts(df):
    return sorted(df['District'].unique().tolist())

def get_talukas(df, district):
    return sorted(df[df['District'] == district]['Taluka'].unique().tolist())

def get_locations(df, district, taluka):
    return sorted(df[(df['District'] == district) & (df['Taluka'] == taluka)]['Location'].unique().tolist())

def get_rate_types():
    return ["Industrial Rate", "Residential Rate", "Commercial Rate"]

def get_rate(df, district, taluka, location, rate_type):
    row = df[
        (df['District'] == district) &
        (df['Taluka'] == taluka) &
        (df['Location'] == location)
    ]
    if row.empty:
        return "No rate found for the selected options."
    rate = row.iloc[0][rate_type]
    return rate if pd.notna(rate) else "Rate not available"

# === CLI Dropdown Simulation ===

# 1. District
districts = get_all_districts(df)
print("\n📍 Districts:")
for i, d in enumerate(districts):
    print(f"{i+1}. {d}")
d_index = int(input("Select District Number: ")) - 1
selected_district = districts[d_index]

# 2. Taluka
talukas = get_talukas(df, selected_district)
print("\n🗺️ Talukas:")
for i, t in enumerate(talukas):
    print(f"{i+1}. {t}")
t_index = int(input("Select Taluka Number: ")) - 1
selected_taluka = talukas[t_index]

# 3. Location
locations = get_locations(df, selected_district, selected_taluka)
print("\n📌 Locations:")
for i, l in enumerate(locations):
    print(f"{i+1}. {l}")
l_index = int(input("Select Location Number: ")) - 1
selected_location = locations[l_index]

# 4. Rate Type
rate_types = get_rate_types()
print("\n💼 Rate Types:")
for i, r in enumerate(rate_types):
    print(f"{i+1}. {r}")
r_index = int(input("Select Rate Type Number: ")) - 1
selected_rate_type = rate_types[r_index]

# 5. Final Rate
final_rate = get_rate(df, selected_district, selected_taluka, selected_location, selected_rate_type)
print(f"\n💰 {selected_rate_type} in {selected_location}, {selected_taluka}, {selected_district} = {final_rate}")
