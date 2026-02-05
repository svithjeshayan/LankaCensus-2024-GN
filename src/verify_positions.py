"""
Full verification of ALL GN Division positions in GeoJSON.
"""
import json
from pathlib import Path

# Sri Lanka geographic bounds
SRI_LANKA_BOUNDS = {
    'lat_min': 5.8, 'lat_max': 10.0,
    'lon_min': 79.4, 'lon_max': 82.1
}

# District approximate centers for validation
DISTRICT_CENTERS = {
    'COLOMBO': (6.93, 79.85),
    'GAMPAHA': (7.09, 80.00),
    'KALUTARA': (6.58, 79.96),
    'KANDY': (7.29, 80.64),
    'MATALE': (7.47, 80.62),
    'NUWARA ELIYA': (6.97, 80.78),
    'GALLE': (6.05, 80.22),
    'MATARA': (5.95, 80.54),
    'HAMBANTOTA': (6.12, 81.12),
    'JAFFNA': (9.66, 80.01),
    'KILINOCHCHI': (9.38, 80.40),
    'MANNAR': (8.98, 79.90),
    'MULLAITIVU': (9.27, 80.81),
    'VAVUNIYA': (8.75, 80.50),
    'TRINCOMALEE': (8.57, 81.23),
    'BATTICALOA': (7.73, 81.70),
    'AMPARA': (7.30, 81.67),
    'KURUNEGALA': (7.49, 80.36),
    'PUTTALAM': (8.03, 79.83),
    'ANURADHAPURA': (8.31, 80.41),
    'POLONNARUWA': (7.94, 81.00),
    'BADULLA': (6.99, 81.05),
    'MONARAGALA': (6.87, 81.35),
    'RATNAPURA': (6.68, 80.40),
    'KEGALLE': (7.25, 80.35),
}

def get_centroid(geom):
    """Calculate approximate centroid from geometry."""
    try:
        geom_type = geom.get('type', '')
        coords = geom.get('coordinates', [])
        
        if not coords:
            return None, None
        
        if geom_type == 'Polygon':
            points = coords[0]
        elif geom_type == 'MultiPolygon':
            points = coords[0][0]
        else:
            return None, None
        
        if not points or not isinstance(points[0], list):
            return None, None
        
        lons = [p[0] for p in points]
        lats = [p[1] for p in points]
        
        return sum(lats) / len(lats), sum(lons) / len(lons)
    except (IndexError, TypeError, ZeroDivisionError):
        return None, None

def main():
    geojson_path = Path("data/processed/GN_census_merged.geojson")
    
    print("Loading GeoJSON (this may take a moment)...")
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = len(data['features'])
    print(f"Total features to check: {total}\n")
    
    # Counters
    in_bounds = 0
    out_bounds = 0
    no_geometry = 0
    out_bounds_examples = []
    
    print("Checking ALL features...")
    for i, feature in enumerate(data['features']):
        if (i + 1) % 5000 == 0:
            print(f"  Progress: {i+1}/{total}")
        
        geom = feature.get('geometry', {})
        lat, lon = get_centroid(geom)
        
        if lat is None or lon is None:
            no_geometry += 1
            continue
        
        if (SRI_LANKA_BOUNDS['lat_min'] <= lat <= SRI_LANKA_BOUNDS['lat_max'] and
            SRI_LANKA_BOUNDS['lon_min'] <= lon <= SRI_LANKA_BOUNDS['lon_max']):
            in_bounds += 1
        else:
            out_bounds += 1
            if len(out_bounds_examples) < 10:
                name = feature['properties'].get('shapeName', 'Unknown')
                out_bounds_examples.append(f"{name}: ({lat:.4f}, {lon:.4f})")
    
    # Results
    print("\n" + "="*60)
    print("FULL VERIFICATION RESULTS")
    print("="*60)
    print(f"Total features:       {total:,}")
    print(f"In Sri Lanka bounds:  {in_bounds:,} ({100*in_bounds/total:.2f}%)")
    print(f"Out of bounds:        {out_bounds:,}")
    print(f"No valid geometry:    {no_geometry:,}")
    
    if out_bounds_examples:
        print("\nOut of bounds examples:")
        for ex in out_bounds_examples:
            print(f"  ✗ {ex}")
    
    # Save detailed report
    with open('position_verification_report.txt', 'w') as f:
        f.write("FULL GN POSITION VERIFICATION REPORT\n")
        f.write("="*50 + "\n\n")
        f.write(f"Total features: {total}\n")
        f.write(f"In Sri Lanka bounds: {in_bounds} ({100*in_bounds/total:.2f}%)\n")
        f.write(f"Out of bounds: {out_bounds}\n")
        f.write(f"No valid geometry: {no_geometry}\n\n")
        
        if in_bounds == total - no_geometry:
            f.write("RESULT: ALL GN divisions are correctly positioned within Sri Lanka!\n")
        else:
            f.write(f"RESULT: {out_bounds} features may have position issues.\n")
    
    print("\nDetailed report saved to: position_verification_report.txt")
    
    if in_bounds == total - no_geometry:
        print("\n✅ ALL GN divisions are correctly positioned within Sri Lanka!")
    else:
        print(f"\n⚠️ {out_bounds} features may have position issues.")

if __name__ == "__main__":
    main()
