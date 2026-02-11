
import pandas as pd
import numpy as np

def clean_and_load_data(file_path):
    # Load dataset, skipping the first 10 rows to get to the header row
    # The header is actually spread across rows, but row 10 (0-indexed) seems to have the main structure for data reading
    # Let's read without header first to control it manually
    df = pd.read_csv(file_path, header=None, skiprows=11)
    
    # Define columns based on visual inspection of the CSV structure
    # 0: Province Code, 1: Province Name, 2: District Code, 3: District Name
    # 13: 0-14, 14: 15-59, 15: 60-64, 16: 65+
    
    df.columns = [
        'Province_Code', 'Province_Name', 'District_Code', 'District_Name',
        'DS_Code', 'DS_Name', 'GN_Code', 'GN_Name', 'GN_Number',
        'Total_Pop_Sex', 'Male', 'Female', 
        'Total_Pop_Age', 'Age_0_14', 'Age_15_59', 'Age_60_64', 'Age_65_Plus'
    ]
    
    # Convert numerical columns to numeric, coercing errors to NaN
    cols_to_numeric = ['Total_Pop_Sex', 'Age_0_14', 'Age_15_59', 'Age_60_64', 'Age_65_Plus']
    for col in cols_to_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    return df

def calculate_district_metrics(df):
    # Group by District
    district_df = df.groupby('District_Name')[['Total_Pop_Sex', 'Age_0_14', 'Age_15_59', 'Age_60_64', 'Age_65_Plus']].sum().reset_index()
    
    # Calculate Derived Metrics
    district_df['Pop_60_Plus'] = district_df['Age_60_64'] + district_df['Age_65_Plus']
    
    # 1. Aging Index: (Pop 60+ / Pop 0-14) * 100
    district_df['Aging_Index'] = (district_df['Pop_60_Plus'] / district_df['Age_0_14']) * 100
    
    # 2. Dependency Ratio (Total): ((Pop 0-14 + Pop 60+) / Pop 15-59) * 100
    district_df['Dependency_Ratio'] = ((district_df['Age_0_14'] + district_df['Pop_60_Plus']) / district_df['Age_15_59']) * 100
    
    # 3. Old Age Dependency Ratio: (Pop 60+ / Pop 15-59) * 100
    district_df['Old_Age_Dependency'] = (district_df['Pop_60_Plus'] / district_df['Age_15_59']) * 100
    
    # 4. Youth Bulge: (Pop 0-14 / Total Pop) * 100
    district_df['Youth_Pct'] = (district_df['Age_0_14'] / district_df['Total_Pop_Sex']) * 100
    
    # 5. Workforce Potential: (Pop 15-59 / Total Pop) * 100
    district_df['Workforce_Pct'] = (district_df['Age_15_59'] / district_df['Total_Pop_Sex']) * 100
    
    return district_df

def print_strategic_insights(district_df):
    output_path = 'analysis_output/executive_insights.txt'
    import os
    os.makedirs('analysis_output', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("--- 🇱🇰 EXECUTIVE INTELLIGENCE REPORT: CENSUS 2024 ---\n\n")
        
        # 1. Aging Crisis Zones (Highest Aging Index)
        f.write("WARNING: Top 5 'Aging Crisis' Districts (Highest Aging Index)\n")
        aging = district_df.sort_values(by='Aging_Index', ascending=False).head(5)
        f.write(aging[['District_Name', 'Aging_Index', 'Old_Age_Dependency', 'Pop_60_Plus']].to_string(index=False))
        f.write("\n\n")
        
        # 2. Future Growth Engines (Highest Youth Population %)
        f.write("OPPORTUNITY: Top 5 'Future Growth Engines' (Highest Youth %)\n")
        youth = district_df.sort_values(by='Youth_Pct', ascending=False).head(5)
        f.write(youth[['District_Name', 'Youth_Pct', 'Age_0_14']].to_string(index=False))
        f.write("\n\n")
        
        # 3. Current Economic Powerhouses (Highest Workforce %)
        f.write("STABILITY: Top 5 'Economic Powerhouses' (Highest Working Age %)\n")
        workforce = district_df.sort_values(by='Workforce_Pct', ascending=False).head(5)
        f.write(workforce[['District_Name', 'Workforce_Pct', 'Dependency_Ratio']].to_string(index=False))
        f.write("\n\n")
        
        # 4. District Ranking Table for Report
        f.write("--- FULL DISTRICT DATA FOR REPORT TABLE ---\n")
        f.write(district_df[['District_Name', 'Total_Pop_Sex', 'Aging_Index', 'Dependency_Ratio', 'Youth_Pct', 'Workforce_Pct']].sort_values(by='Total_Pop_Sex', ascending=False).to_string(index=False))
    
    print(f"Insights written to {output_path}")


if __name__ == "__main__":
    file_path = 'data/raw/GN_population_excel.csv'
    df = clean_and_load_data(file_path)
    district_metrics = calculate_district_metrics(df)
    print_strategic_insights(district_metrics)
