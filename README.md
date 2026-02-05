# LankaCensus-2024-GN Population Analysis

This project analyzes the 2024 Sri Lanka Census data at the GN (Grama Niladhari) Division level. It includes data cleaning, Exploratory Data Analysis (EDA), and Geospatial Analysis.

## Project Structure

The project is organized as follows:

- **`data/`**: Contains raw and processed data.
  - `raw/`: Original datasets (Excel files, shapefiles).
  - `processed/`: Cleaned CSVs and GeoJSON files used for analysis.
- **`notebooks/`**: Jupyter notebooks for interactive analysis.
  - `Sri_Lanka_Census_EDA.ipynb`: Demographic analysis (Age, Sex ratios).
  - `Geospatial_Analysis.ipynb`: Mapping and spatial clustering.
- **`src/`**: Python source code.
  - `clean_census.py`: Script to clean the raw Excel data and populate `data/processed`.
- **`output/`**: Generated artifacts.
  - `images/`: Static plots and maps.
  - `html/`: Interactive HTML maps.

## Setup & Usage

1. **Install Dependencies**:
   Ensure you have Python installed with the necessary libraries (pandas, geopandas, matplotlib, seaborn, folium, sklearn).

2. **Data Preparation**:
   The raw data is located in `data/raw`. If you need to regenerate the processed data, run the cleaning script:

   ```bash
   cd src
   python clean_census.py
   ```

   This will create/update `data/processed/GN_population_cleaned.csv`.

3. **Run Analysis**:
   Open the notebooks in `notebooks/` directory to run the analysis.
   - Start with `Sri_Lanka_Census_EDA.ipynb` for general insights.
   - Run `Geospatial_Analysis.ipynb` for maps.

## Data Sources

- **Census Data**: 2024 Sri Lanka Census (Provisional).
- **Boundaries**: geoBoundaries LKA ADM4 shapefiles.

## Author

- Theepan
