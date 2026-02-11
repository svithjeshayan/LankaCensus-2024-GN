
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Create output directory
os.makedirs("output/linkedin_visuals", exist_ok=True)

# Data from comparison_report_draft.md
data = {
    'District': ['Colombo', 'Trincomalee'],
    'Population': [2375415, 442745],
    'Age_0_to_14': [16.5, 26.1],
    'Age_15_to_59': [64.2, 62.4],
    'Age_60_plus': [19.3, 11.5], 
    'Child_Dependency': [25.6, 40.1],
    'Old_Age_Dependency': [30.9, 20.9],
    'School_Priority': [36.1, 56.5],
    'ElderCare_Priority': [28.9, 19.5],
    'School_Priority_Raw': [36.1296, 56.4936],
    'ElderCare_Priority_Raw': [28.9435, 19.5274]
}

df = pd.DataFrame(data)

# Set style
sns.set_theme(style="whitegrid")
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = ['Arial']

# 1. Population Comparison
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='District', y='Population', data=df, palette=['#1f77b4', '#ff7f0e'])
plt.title('Total Population: Colombo vs Trincomalee (2024)', fontsize=16, weight='bold')
plt.ylabel('Population (Millions)', fontsize=12)
# Format y-axis to M
def millions_formatter(x, pos):
    return f'{x/1e6:.1f}M'
from matplotlib.ticker import FuncFormatter
ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

for i, v in enumerate(df['Population']):
    ax.text(i, v + 50000, f"{v:,.0f}", ha='center', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig('output/linkedin_visuals/01_population_comparison.png', dpi=300)
plt.close()

# 2. Age Structure (Side-by-side bar)
age_long = pd.melt(df, id_vars=['District'], value_vars=['Age_0_to_14', 'Age_15_to_59', 'Age_60_plus'],
                    var_name='Age Group', value_name='Percentage')
# Rename age groups for display
age_long['Age Group'] = age_long['Age Group'].replace({
    'Age_0_to_14': '0-14 (Youth)',
    'Age_15_to_59': '15-59 (Working)',
    'Age_60_plus': '60+ (Elderly)'
})

plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Age Group', y='Percentage', hue='District', data=age_long, palette=['#1f77b4', '#ff7f0e'])
plt.title('Age Structure: Colombo vs Trincomalee', fontsize=16, weight='bold')
plt.ylabel('Percentage (%)', fontsize=12)
plt.legend(title='District')

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', padding=3, fontsize=10)

plt.tight_layout()
plt.savefig('output/linkedin_visuals/02_age_structure.png', dpi=300)
plt.close()


# 3. Dependency Ratios
dep_long = pd.melt(df, id_vars=['District'], value_vars=['Child_Dependency', 'Old_Age_Dependency'],
                   var_name='Dependency Type', value_name='Ratio')
dep_long['Dependency Type'] = dep_long['Dependency Type'].replace({
    'Child_Dependency': 'Child (0-14)',
    'Old_Age_Dependency': 'Old Age (60+)'
})

plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Dependency Type', y='Ratio', hue='District', data=dep_long, palette=['#1f77b4', '#ff7f0e'])
plt.title('Dependency Ratios (Per 100 Working-Age People)', fontsize=16, weight='bold')
plt.ylabel('Ratio', fontsize=12)
plt.legend(title='District')

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', padding=3, fontsize=10)

plt.tight_layout()
plt.savefig('output/linkedin_visuals/03_dependency_ratios.png', dpi=300)
plt.close()

# 4. Priority Scores
prio_long = pd.melt(df, id_vars=['District'], value_vars=['School_Priority_Raw', 'ElderCare_Priority_Raw'],
                    var_name='Priority Type', value_name='Score')
prio_long['Priority Type'] = prio_long['Priority Type'].replace({
    'School_Priority_Raw': 'School Priority',
    'ElderCare_Priority_Raw': 'Elder Care Priority'
})

plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Priority Type', y='Score', hue='District', data=prio_long, palette=['#1f77b4', '#ff7f0e'])
plt.title('Priority Index Scores: Infrastructure Needs', fontsize=16, weight='bold')
plt.ylabel('Priority Score (Normalized)', fontsize=12)
plt.legend(title='District')

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', padding=3, fontsize=10)

plt.tight_layout()
plt.savefig('output/linkedin_visuals/04_priority_comparison.png', dpi=300)
plt.close()

print("Charts generated successfully in output/linkedin_visuals/")
