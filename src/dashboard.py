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
    page_icon="🇱🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Executive Theme ---
st.markdown("""
<style>
    /* Executive Light Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main background */
    /* Main background */
    .stApp {
        background-color: #f8fafc;
        /* Gradient removed to prevent banding issues */
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
    h1, h2, h3 {
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
    
    # Create a normalized column for joining
    df['GN_Link_Key'] = df['GN_Division'].str.upper().str.strip()
    
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
    
    # Normalize keys in GeoJSON to match dataframe
    for feature in data['features']:
        if 'shapeName' in feature['properties']:
             # Create a standardized key in properties for linking
             feature['properties']['shapeName_upper'] = str(feature['properties']['shapeName']).upper().strip()
             
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
        provinces = ["All"] + sorted(df['Province'].dropna().unique().tolist())
        selected_province = st.selectbox("Province", provinces, index=0)
        
        # Filter districts based on province
        if selected_province != "All":
            district_options = ["All"] + sorted(df[df['Province'] == selected_province]['District'].dropna().unique().tolist())
        else:
            district_options = ["All"] + sorted(df['District'].dropna().unique().tolist())
        selected_district = st.selectbox("District", district_options, index=0)
        
        # Filter DS Divisions based on district
        if selected_district != "All":
            ds_options = ["All"] + sorted(df[df['District'] == selected_district]['DS_Division'].dropna().unique().tolist())
        else:
            ds_options = ["All"]
        selected_ds = st.selectbox("DS Division", ds_options, index=0)
        
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
        show_map = st.toggle("Show Map", value=True)
        show_raw_data = st.checkbox("Show Raw Data Table", value=False)
    
    # --- Apply Filters ---
    filtered_df = df.copy()
    if selected_province != "All":
        filtered_df = filtered_df[filtered_df['Province'] == selected_province]
    if selected_district != "All":
        filtered_df = filtered_df[filtered_df['District'] == selected_district]
    if selected_ds != "All":
        filtered_df = filtered_df[filtered_df['DS_Division'] == selected_ds]
    
    # --- Key Metrics Row ---
    st.markdown("### 📈 Key Metrics")
    
    # Calculate totals based on gender/age filters
    total_male = filtered_df['Male'].sum()
    total_female = filtered_df['Female'].sum()
    total_pop = filtered_df['Total_Population'].sum()
    
    # Age group sums
    age_0_14 = filtered_df['Age_0_14'].sum()
    age_15_59 = filtered_df['Age_15_59'].sum()
    age_60_64 = filtered_df['Age_60_64'].sum()
    age_65_plus = filtered_df['Age_65_Plus'].sum()
    
    # Apply gender focus
    if selected_gender == "Male":
        display_pop = total_male
        gender_label = "Male Population"
    elif selected_gender == "Female":
        display_pop = total_female
        gender_label = "Female Population"
    else:
        display_pop = total_pop
        gender_label = "Total Population"
    
    # Apply age group filter (sum selected groups)
    if selected_age_groups:
        age_map = {
            "0-14 (Youth)": age_0_14,
            "15-59 (Working)": age_15_59,
            "60-64": age_60_64,
            "65+ (Elderly)": age_65_plus
        }
        selected_age_pop = sum([age_map[ag] for ag in selected_age_groups])
        age_label = " + ".join([ag.split()[0] for ag in selected_age_groups])
    else:
        selected_age_pop = total_pop
        age_label = "All Ages"
    
    avg_sex_ratio = (total_female / max(total_male, 1) * 100)
    
    # Calculate aggregate dependency ratio (weighted average) instead of mean of ratios
    total_youth = filtered_df['Age_0_14'].sum()
    total_elderly = filtered_df['Age_60_64'].sum() + filtered_df['Age_65_Plus'].sum()
    total_working = filtered_df['Age_15_59'].sum()
    
    # Avoid division by zero
    avg_dependency = ((total_youth + total_elderly) / max(total_working, 1) * 100)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(gender_label, f"{display_pop:,}")
    with col2:
        st.metric(f"Age: {age_label}", f"{selected_age_pop:,}")
    with col3:
        st.metric("Sex Ratio (F/M)", f"{avg_sex_ratio:.1f}")
    with col4:
        st.metric("Avg Dependency %", f"{avg_dependency:.1f}%")
    with col5:
        st.metric("GN Divisions", f"{len(filtered_df):,}")
    
    st.markdown("---")
    
    # --- Geospatial Visualization ---
    if show_map and geojson:
        st.markdown("### 🗺️ Population Density Map")
        
        # Optimization: Only plot if subset is reasonable size, or warn
        if len(filtered_df) > 1000 and selected_district == "All":
             st.info("⚠️ Displaying large dataset on map. Filters recommended for better performance.")
        
        # Center map logic
        if selected_ds != "All":
            center_lat, center_lon = 6.9271, 79.8612 # Default Colombo, simplistic
            zoom = 11
        elif selected_district != "All":
            center_lat, center_lon = 7.8731, 80.7718 # Sri Lanka center roughly
            zoom = 9
        else:
            center_lat, center_lon = 7.8731, 80.7718
            zoom = 7
            
        fig_map = px.choropleth_mapbox(
            filtered_df,
            geojson=geojson,
            locations='GN_Link_Key',
            featureidkey="properties.shapeName_upper",
            color='Total_Population',
            mapbox_style="carto-positron",
            zoom=zoom,
            center={"lat": center_lat, "lon": center_lon},
            opacity=0.6,
            labels={'Total_Population': 'Population', 'GN_Link_Key': 'GN Division'},
            title="Population Distribution",
            color_continuous_scale="Viridis",
            hover_name='GN_Division'
        )
        fig_map.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#1e3a5f',
        )
        st.plotly_chart(fig_map, use_container_width=True)
        st.caption("Note: Map matching is based on GN Division names. Some boundaries may not match perfectly due to naming variations.")
        st.markdown("---")
    elif show_map and not geojson:
        st.warning("⚠️ GeoJSON file not found. Map visualization disabled.")
        st.markdown("---")

    
    # --- Charts Section ---
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 👥 Gender Distribution")
        gender_data = pd.DataFrame({
            'Gender': ['Male', 'Female'],
            'Population': [total_male, total_female]
        })
        fig_gender = px.pie(
            gender_data, 
            values='Population', 
            names='Gender',
            color='Gender',
            color_discrete_map={'Male': '#1e3a5f', 'Female': '#0d9488'},
            hole=0.4
        )
        fig_gender.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#1e3a5f',
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with chart_col2:
        st.markdown("#### 🎂 Age Distribution")
        age_data = pd.DataFrame({
            'Age Group': ['0-14 (Youth)', '15-59 (Working)', '60-64', '65+ (Elderly)'],
            'Population': [
                filtered_df['Age_0_14'].sum(),
                filtered_df['Age_15_59'].sum(),
                filtered_df['Age_60_64'].sum(),
                filtered_df['Age_65_Plus'].sum()
            ]
        })
        fig_age = px.bar(
            age_data,
            x='Age Group',
            y='Population',
            color='Age Group',
            color_discrete_sequence=['#1e3a5f', '#0d9488', '#d97706', '#dc2626']
        )
        fig_age.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#1e3a5f',
            showlegend=False,
            xaxis=dict(gridcolor='#e2e8f0'),
            yaxis=dict(gridcolor='#e2e8f0')
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    # --- Population Pyramid ---
    st.markdown("---")
    st.markdown("### 🔺 Population Pyramid by Age Group")
    
    # Aggregate by age groups for pyramid
    pyramid_data = pd.DataFrame({
        'Age Group': ['0-14', '15-59', '60-64', '65+'],
        'Male': [
            -filtered_df['Age_0_14'].sum() * (total_male / max(total_pop, 1)),
            -filtered_df['Age_15_59'].sum() * (total_male / max(total_pop, 1)),
            -filtered_df['Age_60_64'].sum() * (total_male / max(total_pop, 1)),
            -filtered_df['Age_65_Plus'].sum() * (total_male / max(total_pop, 1))
        ],
        'Female': [
            filtered_df['Age_0_14'].sum() * (total_female / max(total_pop, 1)),
            filtered_df['Age_15_59'].sum() * (total_female / max(total_pop, 1)),
            filtered_df['Age_60_64'].sum() * (total_female / max(total_pop, 1)),
            filtered_df['Age_65_Plus'].sum() * (total_female / max(total_pop, 1))
        ]
    })
    
    fig_pyramid = go.Figure()
    fig_pyramid.add_trace(go.Bar(
        y=pyramid_data['Age Group'],
        x=pyramid_data['Male'],
        name='Male',
        orientation='h',
        marker_color='#1e3a5f'
    ))
    fig_pyramid.add_trace(go.Bar(
        y=pyramid_data['Age Group'],
        x=pyramid_data['Female'],
        name='Female',
        orientation='h',
        marker_color='#0d9488'
    ))
    fig_pyramid.update_layout(
        barmode='overlay',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#1e3a5f',
        xaxis=dict(
            title='Population',
            gridcolor='#e2e8f0',
            tickformat=',d',
            tickvals=[-2000000, -1000000, 0, 1000000, 2000000],
            ticktext=['2M', '1M', '0', '1M', '2M']
        ),
        yaxis=dict(gridcolor='#e2e8f0'),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        height=400
    )
    st.plotly_chart(fig_pyramid, use_container_width=True)
    
    # --- District/DS Level Breakdown ---
    st.markdown("---")
    
    if selected_province != "All" and selected_district == "All":
        st.markdown(f"### 📊 District Breakdown in {selected_province}")
        breakdown = filtered_df.groupby('District').agg({
            'Total_Population': 'sum',
            'Male': 'sum',
            'Female': 'sum',
            'Sex_Ratio': 'mean',
            'Dependency_Ratio': 'mean'
        }).reset_index().sort_values('Total_Population', ascending=False)
        
        fig_breakdown = px.bar(
            breakdown,
            x='District',
            y='Total_Population',
            color='Sex_Ratio',
            color_continuous_scale='Viridis',
            labels={'Total_Population': 'Population', 'Sex_Ratio': 'Sex Ratio'}
        )
        fig_breakdown.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#1e3a5f',
            xaxis=dict(tickangle=-45, gridcolor='#e2e8f0'),
            yaxis=dict(gridcolor='#e2e8f0')
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    elif selected_district != "All" and selected_ds == "All":
        st.markdown(f"### 📊 DS Division Breakdown in {selected_district}")
        breakdown = filtered_df.groupby('DS_Division').agg({
            'Total_Population': 'sum',
            'Male': 'sum',
            'Female': 'sum',
            'Sex_Ratio': 'mean',
            'Dependency_Ratio': 'mean'
        }).reset_index().sort_values('Total_Population', ascending=False)
        
        fig_breakdown = px.bar(
            breakdown.head(20),  # Top 20
            x='DS_Division',
            y='Total_Population',
            color='Dependency_Ratio',
            color_continuous_scale='Viridis',
            labels={'Total_Population': 'Population', 'Dependency_Ratio': 'Dependency %'}
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
        # Provincial overview
        st.markdown("### 🗺️ Provincial Overview")
        province_data = df.groupby('Province').agg({
            'Total_Population': 'sum',
            'Male': 'sum',
            'Female': 'sum'
        }).reset_index().sort_values('Total_Population', ascending=True)
        
        fig_province = px.bar(
            province_data,
            y='Province',
            x='Total_Population',
            orientation='h',
            color='Total_Population',
            color_continuous_scale='Viridis'
        )
        fig_province.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#1e3a5f',
            xaxis=dict(gridcolor='#e2e8f0'),
            yaxis=dict(gridcolor='#e2e8f0'),
            showlegend=False,
            height=500
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
        Data Source: Sri Lanka Census 2024 (Provisional) | Built with Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
