
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Create output directory
os.makedirs("output/linkedin_executive", exist_ok=True)

# Reuse the data loading function for consistency
def clean_and_load_data(file_path):
    df = pd.read_csv(file_path, header=None, skiprows=11)
    df.columns = [
        'Province_Code', 'Province_Name', 'District_Code', 'District_Name',
        'DS_Code', 'DS_Name', 'GN_Code', 'GN_Name', 'GN_Number',
        'Total_Pop_Sex', 'Male', 'Female', 
        'Total_Pop_Age', 'Age_0_14', 'Age_15_59', 'Age_60_64', 'Age_65_Plus'
    ]
    cols_to_numeric = ['Total_Pop_Sex', 'Age_0_14', 'Age_15_59', 'Age_60_64', 'Age_65_Plus']
    for col in cols_to_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

def calculate_district_metrics(df):
    district_df = df.groupby('District_Name')[['Total_Pop_Sex', 'Age_0_14', 'Age_15_59', 'Age_60_64', 'Age_65_Plus']].sum().reset_index()
    district_df['Pop_60_Plus'] = district_df['Age_60_64'] + district_df['Age_65_Plus']
    district_df['Aging_Index'] = (district_df['Pop_60_Plus'] / district_df['Age_0_14']) * 100
    district_df['Youth_Pct'] = (district_df['Age_0_14'] / district_df['Total_Pop_Sex']) * 100
    return district_df

# Load Data
file_path = 'data/raw/GN_population_excel.csv'
df = clean_and_load_data(file_path)
metrics = calculate_district_metrics(df)

# Set Global Style
sns.set_theme(style="whitegrid")
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = ['Arial']
brand_color_primary = "#1f77b4" # Blue
brand_color_secondary = "#ff7f0e" # Orange
brand_color_danger = "#d62728" # Red
brand_color_success = "#2ca02c" # Green

# --- Visual 1: The Demographic Divide (Scatter Plot) ---
plt.figure(figsize=(12, 8))
ax = sns.scatterplot(
    data=metrics, 
    x='Youth_Pct', 
    y='Aging_Index', 
    size='Total_Pop_Sex', 
    sizes=(100, 1000), 
    hue='District_Name', 
    palette='tab20',
    legend=False,
    alpha=0.7
)

# Strategic Quadrants
# Median Youth % ~ 22%, Median Aging Index ~ 80
x_mid = metrics['Youth_Pct'].median()
y_mid = metrics['Aging_Index'].median()

plt.axvline(x=x_mid, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=y_mid, color='gray', linestyle='--', alpha=0.5)

# Annotate Quadrants
plt.text(metrics['Youth_Pct'].max(), metrics['Aging_Index'].max(), "AGING CRISIS ZONE\n(Low Youth, High Aging)", ha='right', va='top', fontsize=12, fontweight='bold', color=brand_color_danger, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
plt.text(metrics['Youth_Pct'].max(), metrics['Aging_Index'].min(), "FUTURE GROWTH ZONE\n(High Youth, Low Aging)", ha='right', va='bottom', fontsize=12, fontweight='bold', color=brand_color_success, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# Annotate ALL districts
for i, row in metrics.iterrows():
    # Label every single point
    plt.text(
        row['Youth_Pct'] + 0.1, 
        row['Aging_Index'] + 0.5, 
        row['District_Name'], 
        fontsize=9, 
        weight='semibold',
        alpha=0.9
    )

plt.title('The Tale of Two Lankas: Mapping Demographic Risk & Opportunity', fontsize=18, weight='bold', pad=20)
plt.xlabel('Youth Population (%)', fontsize=14)
plt.ylabel('Aging Index (Elders per 100 Children)', fontsize=14)
plt.tight_layout()
plt.savefig('output/linkedin_executive/01_demographic_divide_scatter.png', dpi=300)
plt.close()


# --- Visual 2: Top 5 Aging Crisis (Bar Chart) ---
top_aging = metrics.sort_values('Aging_Index', ascending=False).head(5)
plt.figure(figsize=(10, 6))
ax = sns.barplot(
    data=top_aging,
    x='Aging_Index',
    y='District_Name',
    palette='Reds_r'
)
plt.title('🚨 RED ALERT: Top 5 Districts Facing an "Aging Crisis"', fontsize=16, weight='bold')
plt.xlabel('Aging Index (Elders per 100 Children)', fontsize=12)
plt.ylabel(None)
plt.axvline(x=100, color='black', linestyle='--', linewidth=1)
plt.text(105, 0.5, "Risk Threshold (100)", rotation=90, va='center')

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', padding=3, fontsize=11, weight='bold')

plt.tight_layout()
plt.savefig('output/linkedin_executive/02_aging_crisis_bar.png', dpi=300)
plt.close()


# --- Visual 3: Top 5 Future Engines (Bar Chart) ---
top_youth = metrics.sort_values('Youth_Pct', ascending=False).head(5)
plt.figure(figsize=(10, 6))
ax = sns.barplot(
    data=top_youth,
    x='Youth_Pct',
    y='District_Name',
    palette='Greens_r'
)
plt.title('🚀 GREEN LIGHT: Top 5 "Future Growth Engine" Districts', fontsize=16, weight='bold')
plt.xlabel('Youth Population Percentage (%)', fontsize=12)
plt.ylabel(None)

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', padding=3, fontsize=11, weight='bold')

plt.tight_layout()
plt.savefig('output/linkedin_executive/03_growth_engines_bar.png', dpi=300)
plt.close()

print("Executive visuals generated in output/linkedin_executive/")
