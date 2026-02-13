# 🇱🇰 Sri Lanka Census 2024 Dashboard Report

## 1. Executive Summary

The **Sri Lanka Census 2024 Dashboard** is a high-performance, interactive analytical tool designed to visualize and explore demographic data at the Grama Niladhari (GN) Division level. Built using **Streamlit** and **Plotly**, it provides policy-makers, researchers, and government officials with granular insights into population structure, aging trends, and workforce potential across the island.

This report outlines the dashboard's technical architecture, key features, and strategic insights derived from the initial data analysis.

## 2. Technical Architecture

The dashboard is built on a modern, open-source stack designed for speed and interactivity:

- **Framework**: [Streamlit](https://streamlit.io/) (Python-based web app framework).
- **Visualization**: [Plotly Express](https://plotly.com/python/plotly-express/) & Graph Objects for interactive charts and maps.
- **Data Processing**: [Pandas](https://pandas.pydata.org/) for data manipulation and analysis.
- **Geospatial Data**: GeoJSON integration for rendering detailed choropleth maps of GN Divisions.
- **Design System**: Custom CSS implementing a professional "Executive Light/Dark Theme" with a responsive grid layout.

### Data Pipeline

1.  **Raw Data**: Census data is ingested from CSV files (`GN_population_cleaned.csv`).
2.  **Processing**: Data is cleaned, and derived metrics (e.g., Dependency Ratio, Youth Bulge) are calculated on-the-fly or pre-processed.
3.  **Geospatial Mapping**: A custom logic links administrative data (Province, District, DS, GN) with GeoJSON polygons, resolving spatial conflicts (e.g., duplicate GN names) using centroid-based distance validation.

## 3. Key Features

### 🔍 Interactive Filtering

Users can drill down from the national level to specific communities using a hierarchical filter system:

- **Province -> District -> DS Division**: Select specific regions to analyze.
- **Demographic Filters**: Focus on specific Gender groups (Male/Female) or Age Brackets (Youth 0-14, Working 15-59, Elderly 60+).

### 📊 Visualization Suite

- **Choropleth Map**: A color-coded map showing population density and distribution. It dynamically zooms to the selected region (Province, District, or DS Division).
- **Population Pyramid/Structure**: Bar charts visualizing the age distribution (Youth vs. Working vs. Elderly).
- **Gender Distribution**: Donut charts showing the male/female balance.
- **Executive Metrics**: Key Performance Indicators (KPIs) display Total Population, Sex Ratio, and Dependency Ratio instantly.

### 📉 Drill-Down Analytics

- **Regional Comparisons**: When a user selects a Province, the dashboard automatically generates a District-level breakdown. Selecting a District triggers a DS Division comparison.
- **Raw Data Access**: Users can view and export the underlying raw data for further offline analysis.

## 4. Strategic Insights & Findings

Based on the latest data processed by the dashboard's analytical engine, several critical demographic trends have emerged.

### ⚠️ Aging Crisis Zones

The following districts exhibit the highest **Aging Index** (population 60+ per 100 youths), indicating a rapidly aging population that requires immediate policy attention regarding healthcare and pension systems.

| District    | Aging Index | Old Age Dependency | Pop 60+ (Count) |
| :---------- | :---------- | :----------------- | :-------------- |
| **Colombo** | **119.3**   | 30.3%              | 438,701         |
| **Kegalle** | 107.0       | 35.5%              | 183,359         |
| **Gampaha** | 104.7       | 29.9%              | 459,280         |
| **Jaffna**  | 100.1       | 32.3%              | 116,812         |
| **Galle**   | 99.7        | 33.0%              | 218,080         |

> **Insight**: Western and Southern provinces, along with Jaffna, are facing significant demographic shifts towards an elderly population.

### 🚀 Future Growth Engines

These districts have the highest **Youth Percentage** (0-14 years), representing the future workforce reservoir. Investment in education and vocational training here will yield high demographic dividends.

| District        | Youth %   | Youth Population (0-14) |
| :-------------- | :-------- | :---------------------- |
| **Trincomalee** | **26.1%** | 115,588                 |
| **Ampara**      | 25.5%     | 189,975                 |
| **Batticaloa**  | 24.6%     | 146,399                 |
| **Mannar**      | 24.4%     | 30,225                  |
| **Moneragala**  | 23.5%     | 124,232                 |

> **Insight**: The Eastern and Northern provinces are significantly "younger" than the national average, presenting a clear opportunity for workforce development.

### 🏛️ Economic Powerhouses (Stability)

Districts with the highest **Working Age Percentage** (15-59 years) and lowest dependency ratios. These areas are currently driving the nation's economic output.

| District        | Workforce % | Dependency Ratio |
| :-------------- | :---------- | :--------------- |
| **Kilinochchi** | **64.7%**   | 54.6%            |
| **Colombo**     | 64.2%       | 55.7%            |
| **Mullaitivu**  | 63.9%       | 56.6%            |
| **Vavuniya**    | 63.4%       | 57.6%            |
| **Gampaha**     | 63.1%       | 58.4%            |

> **Insight**: While Colombo and Gampaha are aging, they still hold the largest active workforce share, joined by Northern districts which are showing strong workforce recovery.

## 5. Conclusion & Recommendations

The **Census 2024 Dashboard** successfully transforms raw census data into actionable intelligence. By highlighting regional disparities—such as the "Aging Crisis" in the West versus the "Youth Bulge" in the East—it enables targeted resource allocation.

**Next Steps:**

1.  **Predictive Modeling**: Incorporate birth/death rate trends to forecast future populations for 2030.
2.  **Infrastructure Overlay**: Map schools and hospitals against the youth and elderly population layers to identify service gaps.
3.  **Mobile Optimization**: Enhance the UI for field officers accessing data via tablets/phones.

---

_Report generated by Antigravity AI Assistant_
