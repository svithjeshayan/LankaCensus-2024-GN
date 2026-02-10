"""
Sri Lanka Census 2024 - Interactive Dashboard
Analyzes population demographics at the GN Division level.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Sri Lanka Census 2024 Dashboard",
    page_icon="https://e7.pngegg.com/pngimages/944/386/png-clipart-government-of-sri-lanka-government-gazette-indonesia-sri-lanka-relations-others-logo-republic-thumbnail.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS: Executive Theme ---
st.markdown("""
<style>
    /* Executive Light Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Base variables */
    :root {
        --primary-color: #1e3a5f;
        --secondary-color: #0ea5e9;
    }
    
    /* Main background */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Metric cards - Executive style */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-left: 4px solid #1e3a5f;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    div[data-testid="metric-container"] label {
        color: #64748b !important;
        font-weight: 500;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #1e3a5f !important;
        font-weight: 700;
        font-size: 1.8rem;
    }

    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        color: #64748b !important;
    }
    
    /* Sidebar styling - Executive */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stCheckbox label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }
    
    /* Headers - Navy executive style */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a5f !important;
        font-weight: 600;
    }
    
    /* Markdown text */
    .stMarkdown p {
        color: #475569;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        color: #1e3a5f;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }
    
    /* Divider */
    hr {
        border-color: #cbd5e1;
    }
    
    /* Plotly charts text */
    .js-plotly-plot text {
        fill: #1e3a5f !important;
    }
    .js-plotly-plot .gtitle {
        fill: #1e3a5f !important;
    }
    
    /* ===================== DARK MODE SUPPORT ===================== */
    /* Only apply dark theme styling when user explicitly switches to Dark Mode */
    [data-theme="dark"] .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    }
    
    [data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3,
    [data-theme="dark"] h4, [data-theme="dark"] h5, [data-theme="dark"] h6 {
        color: #f1f5f9 !important;
    }
    
    [data-theme="dark"] .stMarkdown p, [data-theme="dark"] .stMarkdown span {
        color: #cbd5e1 !important;
    }
    
    [data-theme="dark"] div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-color: #334155 !important;
        border-left-color: #06b6d4 !important;
    }
    
    [data-theme="dark"] div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
    }
    
    [data-theme="dark"] div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
    }
    
    [data-theme="dark"] div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        color: #cbd5e1 !important;
    }
    
    [data-theme="dark"] section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    }
    
    [data-theme="dark"] .streamlit-expanderHeader {
        background: #1e293b !important;
        border-color: #334155 !important;
        color: #f1f5f9 !important;
    }
    
    [data-theme="dark"] .stDataFrame {
        border-color: #334155 !important;
    }
    
    [data-theme="dark"] .stDataFrame table, [data-theme="dark"] .stDataFrame th, [data-theme="dark"] .stDataFrame td {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
    }
    
    [data-theme="dark"] hr {
        border-color: #475569 !important;
    }
    
    [data-theme="dark"] .js-plotly-plot text {
        fill: #f1f5f9 !important;
    }
    [data-theme="dark"] .js-plotly-plot .gtitle {
        fill: #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Data Loading with Caching ---
@st.cache_data
def load_data():
    """Load and preprocess the census data."""
    # Determine path relative to this script
    script_dir = Path(__file__).parent
    data_path = script_dir.parent / "data" / "processed" / "GN_population_cleaned.csv"
    
    # Load data
    df = pd.read_csv(data_path)
    
    # Clean column names (remove newlines)
    df.columns = df.columns.str.replace('\n', '_').str.replace('\r', '').str.strip()
    
    # Rename columns for easier access
    rename_map = {
        'Province_Code': 'Province_Code',
        'Province_Name': 'Province',
        'District_Code': 'District_Code', 
        'District_Name': 'District',
        'DS_Division_Code': 'DS_Code',
        'DS_Division_Name': 'DS_Division',
        'GN_Division_Code': 'GN_Code',
        'GN_Division_Name': 'GN_Division',
        'GN_Division_Number': 'GN_Number',
        'Sex_Total': 'Total_Population',
        'Sex_Male': 'Male',
        'Sex_Female': 'Female',
        'Age_Total': 'Age_Total',
        'Age_0_to_14': 'Age_0_14',
        'Age_15_to_59': 'Age_15_59',
        'Age_60_to_64': 'Age_60_64',
        'Age_65_and_above': 'Age_65_Plus'
    }
    df = df.rename(columns=rename_map)
    
    # Ensure numeric columns
    numeric_cols = ['Total_Population', 'Male', 'Female', 'Age_0_14', 'Age_15_59', 'Age_60_64', 'Age_65_Plus']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Calculate derived metrics
    df['Sex_Ratio'] = (df['Female'] / df['Male'].replace(0, 1) * 100).round(1)
    df['Youth_Pct'] = (df['Age_0_14'] / df['Total_Population'].replace(0, 1) * 100).round(1)
    df['Working_Age_Pct'] = (df['Age_15_59'] / df['Total_Population'].replace(0, 1) * 100).round(1)
    df['Elderly_Pct'] = ((df['Age_60_64'] + df['Age_65_Plus']) / df['Total_Population'].replace(0, 1) * 100).round(1)
    df['Dependency_Ratio'] = ((df['Age_0_14'] + df['Age_60_64'] + df['Age_65_Plus']) / df['Age_15_59'].replace(0, 1) * 100).round(1)
    
    # Create a composite key for unique GeoJSON joining (District + GN name)
    # GN Division names like 'Mallikaithivu' exist in MULTIPLE districts (Trinco & Mullaitivu).
    # We must include District in the key to ensure the map shows the correct polygon location.
    df['GN_Link_Key'] = (df['District'].str.upper().str.strip() + '|' + df['GN_Division'].str.upper().str.strip())
    
    return df

@st.cache_data
def load_geojson():
    """Load GeoJSON for map visualization."""
    script_dir = Path(__file__).parent
    geojson_path = script_dir.parent / "data" / "processed" / "GN_census_merged.geojson"
    
    if not geojson_path.exists():
        return None
        
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create composite key in GeoJSON to match dataframe (District + GN name)
    # This prevents the map from picking the wrong polygon (e.g. picking Mullaitivu's 'Mallikaithivu'
    # when you selected Trincomalee)
    for feature in data['features']:
        props = feature['properties']
        district = str(props.get('District_Name', '')).upper().strip()
        gn_name = str(props.get('shapeName', '')).upper().strip()
        props['District_GN_Key'] = district + '|' + gn_name
             
    return data

# --- Main App ---
def main():
    # Load data
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("❌ Data file not found. Please ensure `GN_population_cleaned.csv` exists in `data/processed/`.")
        st.stop()
        
    geojson = load_geojson()
    
    # --- Header ---
    st.markdown("""
    <div style='text-align: center; padding: 30px 0; border-bottom: 2px solid #1e3a5f;'>
        <h1 style='font-size: 2.5rem; color: #1e3a5f; margin-bottom: 0; font-weight: 700;'>
            🇱🇰 Sri Lanka Census 2024
        </h1>
        <p style='color: #64748b; font-size: 1.1rem; margin-top: 8px; font-weight: 400;'>
            Population Demographics at Grama Niladhari Division Level
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Sidebar Filters ---
    with st.sidebar:
        st.markdown("### 🔍 Filters")
        
        # Province filter
        provinces = sorted(df['Province'].dropna().unique().tolist())
        selected_provinces = st.multiselect("Select Province(s)", provinces, default=[])
        
        # Filter districts based on province
        if selected_provinces:
            district_options = sorted(df[df['Province'].isin(selected_provinces)]['District'].dropna().unique().tolist())
        else:
            district_options = sorted(df['District'].dropna().unique().tolist())
            
        selected_districts = st.multiselect("Select District(s)", district_options, default=[])
        
        # Filter DS Divisions based on district
        # Only show DS options if districts are selected to avoid huge lists, 
        # or if specific provinces selected (optional, sticking to District dependency for performance)
        if selected_districts:
            ds_options = sorted(df[df['District'].isin(selected_districts)]['DS_Division'].dropna().unique().tolist())
        elif selected_provinces: # Allow DS selection if Province is selected too
            ds_options = sorted(df[df['Province'].isin(selected_provinces)]['DS_Division'].dropna().unique().tolist())
        else:
            ds_options = [] # Hide DS options if no upper level selected to encourage drill-down.
            
        if ds_options:
            selected_ds = st.multiselect("Select DS Division(s)", ds_options, default=[])
        else:
            selected_ds = []
            if not selected_provinces and not selected_districts:
                st.info("Select a Province or District to view DS Divisions")
        
        st.markdown("---")
        st.markdown("### 👤 Demographics")
        
        # Gender filter
        gender_options = ["All", "Male", "Female"]
        selected_gender = st.selectbox("Focus Gender", gender_options, index=0)
        
        # Age group filter
        age_group_options = ["All", "0-14 (Youth)", "15-59 (Working)", "60-64", "65+ (Elderly)"]
        selected_age_groups = st.multiselect(
            "Age Groups", 
            age_group_options[1:],  # Exclude "All" from multiselect
            default=[]
        )
        
        st.markdown("---")
        st.markdown("### 📊 View Options")
        show_map = st.toggle("Show Map", value=False) # Default Disabled
        show_raw_data = st.checkbox("Show Raw Data Table", value=False)
    
    # --- Apply Filters ---
    filtered_df = df.copy()
    if selected_provinces:
        filtered_df = filtered_df[filtered_df['Province'].isin(selected_provinces)]
    if selected_districts:
        filtered_df = filtered_df[filtered_df['District'].isin(selected_districts)]
    if selected_ds:
        filtered_df = filtered_df[filtered_df['DS_Division'].isin(selected_ds)]
    
    # --- Determine display population based on gender/age filters ---
    # Map age group labels to column names
    age_group_col_map = {
        "0-14 (Youth)": "Age_0_14",
        "15-59 (Working)": "Age_15_59",
        "60-64": "Age_60_64",
        "65+ (Elderly)": "Age_65_Plus"
    }
    
    # Calculate the "display population" based on filters
    if selected_age_groups:
        # Sum only selected age group columns
        age_cols = [age_group_col_map[ag] for ag in selected_age_groups]
        filtered_df['Display_Population'] = filtered_df[age_cols].sum(axis=1)
    else:
        # Use total population when no age filter
        filtered_df['Display_Population'] = filtered_df['Total_Population']
    
    # Apply gender filter (note: gender breakdown by age is not in the dataset, 
    # so this applies to age "All" or as an approximate indicator)
    if selected_gender == "Male":
        # When age groups selected, we can only approximate since we don't have gender x age breakdown
        if not selected_age_groups:
            filtered_df['Display_Population'] = filtered_df['Male']
    elif selected_gender == "Female":
        if not selected_age_groups:
            filtered_df['Display_Population'] = filtered_df['Female']
    
    # --- Key Metrics Row ---
    st.markdown("### 📈 Key Metrics")
    
    # Calculate totals based on gender/age filters
    total_male = filtered_df['Male'].sum()
    total_female = filtered_df['Female'].sum()
    total_pop = filtered_df['Total_Population'].sum()
    display_pop = filtered_df['Display_Population'].sum()
    
    # Age group sums
    age_0_14 = filtered_df['Age_0_14'].sum()
    age_15_59 = filtered_df['Age_15_59'].sum()
    age_60_64 = filtered_df['Age_60_64'].sum()
    age_65_plus = filtered_df['Age_65_Plus'].sum()
    
    # Determine metric labels based on filters
    pop_label = "Total Population"
    if selected_age_groups:
        age_labels = [ag.split(" ")[0] for ag in selected_age_groups]  # Get just the age range
        pop_label = f"Population ({', '.join(age_labels)})"
    if selected_gender != "All":
        pop_label = f"{selected_gender} {pop_label}"
    
    # Display Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Show filtered population as primary metric
        pct_of_total = (display_pop / total_pop * 100) if total_pop > 0 else 0
        delta_str = f"{pct_of_total:.1f}% of total" if (selected_age_groups or selected_gender != "All") else None
        st.metric(label=pop_label, value=f"{display_pop:,.0f}", delta=delta_str)
    with col2:
        st.metric(label="Male Population", value=f"{total_male:,.0f}", delta=f"{(total_male/total_pop)*100:.1f}%" if total_pop > 0 else "0%")
    with col3:
        st.metric(label="Female Population", value=f"{total_female:,.0f}", delta=f"{(total_female/total_pop)*100:.1f}%" if total_pop > 0 else "0%")
    with col4:
        # Dependency Ratio: (Age 0-14 + Age 65+) / Age 15-59 * 100
        # Determine dependents and working age from current filtered data
        dependents = age_0_14 + age_65_plus
        working_pop = age_15_59 + age_60_64 # Using 15-64 as working age for dependency ratio
        dep_ratio = (dependents / working_pop * 100) if working_pop > 0 else 0
        st.metric(label="Dependency Ratio", value=f"{dep_ratio:.1f}%")

    st.markdown("---")
    
    # --- Charts & Visualization Section ---
    
    # Pre-calculate Figures to separate logic from layout
    
    # 1. Gender Donut
    # Note: Dataset doesn't have gender x age breakdown, so gender chart shows totals
    gender_note = None
    if selected_age_groups:
        gender_note = "⚠️ Gender data is for all ages (breakdown by age not available)"
    
    labels = ['Male', 'Female']
    values = [total_male, total_female]
    fig_gender = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=['#0ea5e9', '#ec4899'])])
    fig_gender.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#1e3a5f',
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=30, b=0, l=0, r=0),
        height=300
    )

    # 2. Population Structure (Pyramid or Bar)
    # Determine which age groups are selected for highlighting
    selected_age_labels = [ag.split(" ")[0] for ag in selected_age_groups] if selected_age_groups else []
    
    # Set colors - highlight selected, dim others
    default_colors = ['#6366f1', '#10b981', '#f59e0b', '#64748b']
    age_labels = ['0-14', '15-59', '60-64', '65+']
    
    if selected_age_groups:
        # Highlight selected age groups, dim unselected
        colors = [
            default_colors[i] if age_labels[i] in selected_age_labels else '#d1d5db'
            for i in range(4)
        ]
    else:
        colors = default_colors
    
    age_df = pd.DataFrame({
        'Age Group': age_labels,
        'Population': [age_0_14, age_15_59, age_60_64, age_65_plus],
        'Selected': [label in selected_age_labels for label in age_labels] if selected_age_groups else [True]*4
    })
    
    fig_age = px.bar(
        age_df,
        x='Population',
        y='Age Group',
        orientation='h',
        color='Age Group',
        color_discrete_sequence=colors,
        text='Population'
    )
    fig_age.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#1e3a5f',
        xaxis_title="Population",
        showlegend=False,
        height=300,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    # --- Dynamic Layout Logic ---
    if show_map and geojson:
        # Layout: Map (Left) | Gender (Right) -> Age (Bottom)
        col_left, col_right = st.columns([1.5, 1])
        
        with col_left:
            st.markdown("### 🗺️ Population Density")
            
            # Center map logic
            center_lat, center_lon = 7.8731, 80.7718 # Default Sri Lanka center
            zoom = 7
            
            # Adjust zoom/center if specific areas are selected
            if selected_ds and not filtered_df.empty:
                first_ds = filtered_df[filtered_df['DS_Division'].isin(selected_ds)].iloc[0]
                # Approximation if Lat/Lon available in DF, else default
                if 'Latitude' in filtered_df.columns:
                     center_lat = filtered_df[filtered_df['DS_Division'].isin(selected_ds)]['Latitude'].mean()
                     center_lon = filtered_df[filtered_df['DS_Division'].isin(selected_ds)]['Longitude'].mean()
                zoom = 10
            elif selected_districts and not filtered_df.empty:
                if 'Latitude' in filtered_df.columns:
                     center_lat = filtered_df[filtered_df['District'].isin(selected_districts)]['Latitude'].mean()
                     center_lon = filtered_df[filtered_df['District'].isin(selected_districts)]['Longitude'].mean()
                zoom = 9

            # Optimization check
            if len(filtered_df) > 1000 and not selected_districts and not selected_ds:
                 st.info("⚠️ Large dataset. Filter to improve map performance.")

            fig_map = px.choropleth_mapbox(
                filtered_df,
                geojson=geojson,
                locations='GN_Link_Key',
                featureidkey="properties.District_GN_Key",
                color='Display_Population',
                mapbox_style="carto-positron",
                zoom=zoom,
                center={"lat": center_lat, "lon": center_lon},
                opacity=0.7,
                labels={'Display_Population': 'Population'},
                color_continuous_scale="RdYlGn_r",  # Green (low) to Red (high) density
            )
            fig_map.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig_map, use_container_width=True)
            
        with col_right:
            st.markdown("### ⚧ Gender Dist.")
            if gender_note:
                st.caption(gender_note)
            st.plotly_chart(fig_gender, use_container_width=True)
            
        # Age Structure (Full Width below Map/Gender)
        st.markdown("### 👥 Age Structure")
        st.plotly_chart(fig_age, use_container_width=True)

    else:
        # Layout: Gender (Left) | Age (Right) -> Balanced Grid
        if show_map and not geojson:
            st.warning("⚠️ Map data not available.")
            
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### ⚧ Gender Distribution")
            if gender_note:
                st.caption(gender_note)
            st.plotly_chart(fig_gender, use_container_width=True)
        with c2:
            st.markdown("### 👥 Age Structure")
            st.plotly_chart(fig_age, use_container_width=True)
    
    # --- District/DS Level Breakdown ---
    st.markdown("---")
    
    # Logic for Drill-down Charts
    # 1. If Provinces selected (but no districts): Show District Breakdown
    # 2. If Districts selected (but no DS): Show DS Breakdown
    # 3. Else: Show Top Level Overview
    
    if selected_provinces and not selected_districts:
        province_names = ", ".join(selected_provinces)
        if len(selected_provinces) > 3: province_names = f"{len(selected_provinces)} Provinces"
        st.markdown(f"### 📊 District Breakdown in {province_names}")
        
        breakdown = filtered_df.groupby('District').agg({
            'Display_Population': 'sum',
            'Total_Population': 'sum',
            'Male': 'sum',
            'Female': 'sum',
            'Sex_Ratio': 'mean',
            'Dependency_Ratio': 'mean'
        }).reset_index().sort_values('Display_Population', ascending=False)
        
        fig_breakdown = px.bar(
            breakdown,
            x='District',
            y='Display_Population',
            color='Sex_Ratio',
            color_continuous_scale='Viridis',
            labels={'Display_Population': 'Population', 'Sex_Ratio': 'Sex Ratio'}
        )
        fig_breakdown.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#1e3a5f',
            xaxis=dict(tickangle=-45, gridcolor='#e2e8f0'),
            yaxis=dict(gridcolor='#e2e8f0')
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    elif selected_districts and not selected_ds:
        district_names = ", ".join(selected_districts)
        if len(selected_districts) > 3: district_names = f"{len(selected_districts)} Districts"
        st.markdown(f"### 📊 DS Division Breakdown in {district_names}")
        
        breakdown = filtered_df.groupby('DS_Division').agg({
            'Display_Population': 'sum',
            'Total_Population': 'sum',
            'Male': 'sum',
            'Female': 'sum',
            'Sex_Ratio': 'mean',
            'Dependency_Ratio': 'mean'
        }).reset_index().sort_values('Display_Population', ascending=False)
        
        # Limit if too many
        if len(breakdown) > 30:
            st.caption(f"Showing Top 30 of {len(breakdown)} DS Divisions")
            breakdown = breakdown.head(30)
            
        fig_breakdown = px.bar(
            breakdown,
            x='DS_Division',
            y='Display_Population',
            color='Dependency_Ratio',
            color_continuous_scale='Viridis',
            labels={'Display_Population': 'Population', 'Dependency_Ratio': 'Dependency %'}
        )
        fig_breakdown.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#1e3a5f',
            xaxis=dict(tickangle=-45, gridcolor='#e2e8f0'),
            yaxis=dict(gridcolor='#e2e8f0')
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    else:
        # Default Overview (No filters OR Deepest filters active)
        # Included new Drill-down logic logic from previous turn
        
        st.markdown("### 🗺️ Census Overview")
        
        view_level = st.radio(
            "Categorize by:",
            ["Province", "District", "DS Division"],
            horizontal=True,
            key="overview_view_level"
        )
        
        col_map = {
            "Province": "Province",
            "District": "District",
            "DS Division": "DS_Division"
        }
        
        group_col = col_map[view_level]
        
        # Aggregation - use filtered_df with Display_Population for proper filter response
        overview_data = filtered_df.groupby(group_col).agg({
            'Display_Population': 'sum',
            'Total_Population': 'sum',
            'Male': 'sum',
            'Female': 'sum'
        }).reset_index().sort_values('Display_Population', ascending=True)
        
        # Limit for DS Division to avoid overcrowding
        if view_level == "DS Division":
            # Showing top 20 for readability
            st.caption("Showing Top 20 DS Divisions by Population")
            overview_data = overview_data.tail(20)
            
        fig_province = px.bar(
            overview_data,
            y=group_col,
            x='Display_Population',
            orientation='h',
            color='Display_Population',
            color_continuous_scale='Viridis',
            labels={'Display_Population': 'Population', group_col: view_level}
        )
        
        fig_province.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#1e3a5f',
            xaxis=dict(gridcolor='#e2e8f0'),
            yaxis=dict(gridcolor='#e2e8f0'),
            showlegend=False,
            height=500 + (200 if view_level == "District" else 0) # Taller for Districts
        )
        st.plotly_chart(fig_province, use_container_width=True)
    
    # --- Raw Data Table ---
    if show_raw_data:
        st.markdown("---")
        st.markdown("### 📋 Raw Data")
        display_cols = ['Province', 'District', 'DS_Division', 'GN_Division', 
                       'Total_Population', 'Male', 'Female', 'Sex_Ratio',
                       'Age_0_14', 'Age_15_59', 'Age_60_64', 'Age_65_Plus', 'Dependency_Ratio']
        available_cols = [c for c in display_cols if c in filtered_df.columns]
        st.dataframe(
            filtered_df[available_cols].head(100),
            use_container_width=True,
            height=400
        )
        st.caption(f"Showing {min(100, len(filtered_df))} of {len(filtered_df)} records")
    
    # --- Footer ---
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 0.85rem; padding: 20px;'>
        Data Source: Sri Lanka Census 2024 (Provisional) | Built with Streamlit & Plotly<br>
        <span style='color: #1e3a5f; font-weight: 500;'>Author: Vithjeshayan S</span>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
