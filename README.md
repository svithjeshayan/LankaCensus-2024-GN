# Sri Lanka 2024 Census - GN Level Analysis

Comprehensive data science analysis of the **2024 Sri Lanka Census** at the **Grama Niladhari (GN)** level (14,021 divisions).

## Project Overview

This project performs hyper-local demographic analysis including:

- **Sex Ratio Analysis** - Gender balance across GN divisions
- **Dependency Ratios** - Child and Old-Age dependency per working-age population
- **K-Means Clustering** - Demographic profiles (Aging Villages, Young Families, etc.)
- **Resource Allocation** - Priority ranking for schools and elder care facilities
- **Geospatial Mapping** - Choropleth maps and interactive visualizations

## Files

| File                                  | Description                                           |
| ------------------------------------- | ----------------------------------------------------- |
| `Sri_Lanka_Census_EDA.ipynb`          | Main EDA notebook with clustering & anomaly detection |
| `Geospatial_Analysis.ipynb`           | Choropleth maps using GeoPandas and Folium            |
| `GN_population_excel.xlsx`            | Original census data                                  |
| `GN_population_cleaned.csv`           | Cleaned dataset with standardized headers             |
| `GN_population_final_analysis.csv`    | Full dataset with calculated ratios and clusters      |
| `geoBoundaries-LKA-ADM4_simplified.*` | GN Division boundary files                            |

## Requirements

```bash
pip install pandas numpy matplotlib seaborn scikit-learn geopandas folium mapclassify
```

## Data Sources

- Census Data: [Department of Census and Statistics Sri Lanka](https://www.statistics.gov.lk)
- GN Boundaries: [geoBoundaries](https://www.geoboundaries.org/) / [HDX](https://data.humdata.org)

## Key Outputs

- Dependency ratio choropleth maps (PNG)
- Interactive HTML map (`interactive_map_old_age.html`)
- Demographic cluster visualizations
- Priority rankings for resource allocation

## License

Data is sourced from official government statistics and open geospatial datasets.
