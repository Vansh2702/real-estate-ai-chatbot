import pandas as pd

# Load the manually edited Excel file
file_path = "/mnt/data/MIDC RATES.xlsx"
df = pd.read_excel(file_path)

# Show columns
print("📄 Columns:")
print(df.columns.tolist())

# Show unique districts
print("\n🏙️ Districts:")
print(sorted(df['District'].dropna().unique().tolist()))

# Preview a few rows
print("\n🔍 Preview:")
print(df.head())
