import pandas as pd
import numpy as np

file_path = "../data/raw/GN_population_excel.xlsx"
output_path = "../data/processed/GN_population_cleaned.csv"

def clean_and_convert(val):
    """Clean numeric strings with commas and convert to int."""
    if pd.isna(val) or val == ' ':
        return 0
    if isinstance(val, (int, float)):
        return int(val)
    # Remove commas and whitespace
    clean_str = str(val).replace(',', '').strip()
    try:
        return int(clean_str)
    except ValueError:
        return 0

try:
    print("Reading Excel file...")
    # Read full file without headers first to locate data
    df_raw = pd.read_excel(file_path, sheet_name='Population', header=None)
    
    # Locate the header row containing "Province Code"
    header_idx = -1
    for i, row in df_raw.iterrows():
        if "Province Code" in str(row.values):
            header_idx = i
            break
            
    if header_idx == -1:
        raise ValueError("Could not find header row starting with 'Province Code'")
        
    print(f"Headers found at row {header_idx}")
    
    # The actual data usually starts 2 rows after 'Province Code' row in this provisional layout?
    # Based on user sample: 
    # Row 3: Headers (Province Code...)
    # Row 4: Sub-headers (Total, Male...)
    # Row 5: Data
    data_start_idx = header_idx + 2 
    
    # Extract data slice
    df_data = df_raw.iloc[data_start_idx:].copy()
    
    # Check if we need to adjust columns. 
    # We will select columns by index as they are structural.
    # Indices based on user sample (0-based):
    # 0: Province Code
    # 1: Province
    # 2: District Code
    # 3: District Name
    # 4: DS_Division Code
    # 5: DS_Division Name
    # 6: GN_Division Code
    # 7: GN_Division Name
    # 8: GN_Division Number
    # 9: Total_Pop (Sex>Total)
    # 10: Male
    # 11: Female
    # 12: Age_Total (Redundant) - SKIP
    # 13: Age_0_14
    # 14: Age_15_59
    # 15: Age_60_64
    # 16: Age_65_Plus
    
    selected_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16]
    new_columns = [
        "Province_Code", "Province_Name", 
        "District_Code", "District_Name", 
        "DS_Code", "DS_Name", 
        "GN_Code", "GN_Name", "GN_Number",
        "Total_Population", "Male", "Female",
        "Age_0_14", "Age_15_59", "Age_60_64", "Age_65_Plus"
    ]
    
    # Filter columns
    df_clean = df_data.iloc[:, selected_indices].copy()
    df_clean.columns = new_columns
    
    # Drop rows where essential identifiers are missing (e.g. totals rows or empty lines)
    # Ensure GN_Code is present
    df_clean = df_clean.dropna(subset=['GN_Code'])
    
    # Convert numeric columns
    numeric_cols = ["Total_Population", "Male", "Female", "Age_0_14", "Age_15_59", "Age_60_64", "Age_65_Plus"]
    
    for col in numeric_cols:
        df_clean[col] = df_clean[col].apply(clean_and_convert)
        
    # Verify Total Population integrity
    # Check if Male + Female ~= Total
    df_clean['Sex_Sum'] = df_clean['Male'] + df_clean['Female']
    mismatch_sex = df_clean[df_clean['Total_Population'] != df_clean['Sex_Sum']]
    if not mismatch_sex.empty:
        print(f"Warning: {len(mismatch_sex)} rows have mismatching Sex sums.")
        
    # Check Age Sum
    df_clean['Age_Sum'] = df_clean['Age_0_14'] + df_clean['Age_15_59'] + df_clean['Age_60_64'] + df_clean['Age_65_Plus']
    mismatch_age = df_clean[df_clean['Total_Population'] != df_clean['Age_Sum']]
    if not mismatch_age.empty:
        print(f"Warning: {len(mismatch_age)} rows have mismatching Age sums.")
        
    # Drop check columns
    df_clean.drop(columns=['Sex_Sum', 'Age_Sum'], inplace=True)
    
    print("\nSample Data:")
    print(df_clean.head())
    
    print(f"\nSaving to {output_path}...")
    df_clean.to_csv(output_path, index=False)
    print("Done.")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
