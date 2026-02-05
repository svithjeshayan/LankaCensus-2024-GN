import pandas as pd
import json

# Load CSV
csv_path = 'data/processed/GN_population_cleaned.csv'
df = pd.read_csv(csv_path)

# Clean column names same as dashboard
df.columns = df.columns.str.replace('\n', '_').str.replace('\r', '').str.strip()
df = df.rename(columns={'DS_Division_Name': 'DS_Division', 'GN_Division_Name': 'GN_Division'})

# Filter for a sample DS Division to narrow down the noise
# 'Thimbirigasyaya' is a good candidate from previous `view_file`
target_ds = 'Colombo' 
df_subset = df[df['DS_Division'].str.strip() == target_ds].copy()

if df_subset.empty:
    print(f"Warning: No data found for DS Division '{target_ds}'. Using full dataset sample.")
    df_subset = df.head(50)

csv_names = set(df_subset['GN_Division'].astype(str).str.strip().str.upper())

# Load GeoJSON
geojson_path = 'data/processed/GN_census_merged.geojson'
with open(geojson_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract GeoJSON properties
geo_names = set()
for f in data['features']:
    p = f['properties']
    if p.get('shapeName'):
        geo_names.add(str(p['shapeName']).strip().upper())

# Find mismatches
missing_in_map = csv_names - geo_names
found_in_map = csv_names.intersection(geo_names)

with open('mismatch_report.txt', 'w') as f:
    f.write(f"--- Analysis for DS: {target_ds} ---\n")
    f.write(f"Total GN in CSV: {len(csv_names)}\n")
    f.write(f"Successfully Matched: {len(found_in_map)}\n")
    f.write(f"Missing in Map (CSV has it, Map doesn't): {len(missing_in_map)}\n\n")
    
    f.write("--- Missing Examples (CSV Names) ---\n")
    for name in sorted(list(missing_in_map))[:20]:
        f.write(f"'{name}'\n")
        
    f.write("\n--- Available Map Names (Sample likely matches) ---\n")
    # Try to find similar names in map for the missing ones (simple fuzzy check)
    for missing in list(missing_in_map)[:5]:
        f.write(f"\nLooking for matches for: '{missing}'\n")
        candidates = [n for n in geo_names if missing[:4] in n]
        for c in candidates[:5]:
            f.write(f"  Candidate: '{c}'\n")
