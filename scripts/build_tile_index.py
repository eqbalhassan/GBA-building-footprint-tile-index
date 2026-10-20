#!/usr/bin/env python3
"""
build_tile_index.py
===================
Reproducible builder script for the GlobalBuildingAtlas (GBA.ODbLPolygon) 5° x 5°
building-footprint tile index.

Queries the Hugging Face Dataset API for all seven continental subdirectories:
  africa, asiaeast, asiawest, europe, northamerica, oceania, southamerica

Extracts file metadata (bounding coordinates, file size, download URL), constructs
EPSG:4326 polygon geometries, and exports:
  1. ESRI Shapefile (.shp, .shx, .dbf, .prj, .cpg)
  2. GeoJSON (.geojson)
  3. CSV (.csv with xmin, ymin, xmax, ymax columns)

Usage:
  python build_tile_index.py --out building_footprint
  python build_tile_index.py --out building_footprint --csv-out tile_index.csv
"""

import argparse
import os
import re
import sys
import logging
import requests
from typing import List, Dict, Any, Optional

try:
    from shapely.geometry import box
    import geopandas as gpd
    import pandas as pd
except ImportError:
    print(
        "ERROR: This script requires 'geopandas' and 'shapely'.\n"
        "Install dependencies via: pip install -r scripts/requirements.txt",
        file=sys.stderr
    )
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("build_tile_index")

REGIONS = [
    "africa",
    "asiaeast",
    "asiawest",
    "europe",
    "northamerica",
    "oceania",
    "southamerica"
]

API_BASE = "https://huggingface.co/api/datasets/zhu-xlab/GBA.ODbLPolygon/tree/main"
DOWNLOAD_BASE = "https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main"

# Regex matching 5° x 5° tile naming convention:
# e.g., e000_n10_e005_n05.geojson
TILE_REGEX = re.compile(
    r"^([ew])(\d+)_([ns])(\d+)_([ew])(\d+)_([ns])(\d+)\.geojson$",
    re.IGNORECASE
)


def parse_tile_bounds(filename: str):
    """
    Parses a tile filename into signed geographic bounds (minx, miny, maxx, maxy).
    Naming convention: {e|w}{lon_min}_{n|s}{lat_max}_{e|w}{lon_max}_{n|s}{lat_min}.geojson
    Example: e000_n10_e005_n05 -> lon 0 to 5, lat 5 to 10.
    """
    match = TILE_REGEX.match(filename)
    if not match:
        return None

    h1, v1, h2, v2, h3, v3, h4, v4 = match.groups()
    lon_min = -float(v1) if h1.lower() == "w" else float(v1)
    lat_max = -float(v2) if h2.lower() == "s" else float(v2)
    lon_max = -float(v3) if h3.lower() == "w" else float(v3)
    lat_min = -float(v4) if h4.lower() == "s" else float(v4)

    return lon_min, lat_min, lon_max, lat_max


def fetch_region_tiles(region: str, session: requests.Session) -> List[Dict[str, Any]]:
    """
    Fetches the directory listing for a region via the Hugging Face Tree API,
    traversing HTTP Link header pagination (rel="next").
    """
    url = f"{API_BASE}/{region}?limit=1000"
    region_records = []

    logger.info("Fetching tiles for region '%s'...", region)
    while url:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        items = resp.json()

        for item in items:
            if item.get("type") != "file":
                continue

            path = item.get("path", "")
            filename = os.path.basename(path)
            bounds = parse_tile_bounds(filename)
            if not bounds:
                continue

            minx, miny, maxx, maxy = bounds
            tile_name = filename[:-8]  # strip '.geojson'
            size_bytes = item.get("size", 0)
            size_mb = round(size_bytes / (1024.0 * 1024.0), 3)

            download_url = f"{DOWNLOAD_BASE}/{region}/{filename}?download=true"

            region_records.append({
                "region": region,
                "tile": tile_name,
                "size_mb": size_mb,
                "url": download_url,
                "xmin": minx,
                "ymin": miny,
                "xmax": maxx,
                "ymax": maxy,
                "geometry": box(minx, miny, maxx, maxy)
            })

        # Check for pagination in Link header
        if "next" in resp.links:
            url = resp.links["next"]["url"]
        else:
            url = None

    logger.info("Found %d tiles in region '%s'", len(region_records), region)
    return region_records


def build_index(out_dir: str, csv_path: Optional[str] = None):
    """
    Builds the complete spatial tile index and writes shapefile, GeoJSON, and CSV.
    """
    os.makedirs(out_dir, exist_ok=True)

    session = requests.Session()
    all_records = []

    for region in REGIONS:
        records = fetch_region_tiles(region, session)
        all_records.extend(records)

    logger.info("Total tiles harvested across all regions: %d", len(all_records))
    if not all_records:
        logger.error("No tile records found. Exiting.")
        sys.exit(1)

    # Construct GeoDataFrame in EPSG:4326
    gdf = gpd.GeoDataFrame(all_records, crs="EPSG:4326")

    # Shapefile export requires field names <= 10 characters and 2D geometry
    shp_cols = ["region", "tile", "size_mb", "url", "geometry"]
    shp_gdf = gdf[shp_cols].copy()

    shp_out = os.path.join(out_dir, "GBA_ODbLPolygon_grid.shp")
    logger.info("Writing Shapefile to '%s'...", shp_out)
    shp_gdf.to_file(shp_out, driver="ESRI Shapefile", encoding="utf-8")

    geojson_out = os.path.join(out_dir, "GBA_ODbLPolygon_grid.geojson")
    logger.info("Writing GeoJSON to '%s'...", geojson_out)
    shp_gdf.to_file(geojson_out, driver="GeoJSON")

    # CSV Export includes bounding coordinate columns
    if not csv_path:
        csv_path = os.path.join(os.path.dirname(os.path.abspath(out_dir)), "tile_index.csv")

    logger.info("Writing CSV to '%s'...", csv_path)
    csv_cols = ["region", "tile", "size_mb", "url", "xmin", "ymin", "xmax", "ymax"]
    df_csv = pd.DataFrame(gdf[csv_cols])
    df_csv.to_csv(csv_path, index=False)

    logger.info("Build completed successfully. %d features written.", len(gdf))


def main():
    parser = argparse.ArgumentParser(
        description="Build spatial index for GBA.ODbLPolygon building-footprint dataset."
    )
    parser.add_argument(
        "--out",
        default="building_footprint",
        help="Output directory for Shapefile and GeoJSON (default: building_footprint)"
    )
    parser.add_argument(
        "--csv-out",
        default=None,
        help="Output path for CSV index (default: tile_index.csv in parent of --out)"
    )
    args = parser.parse_args()

    build_index(args.out, args.csv_out)


if __name__ == "__main__":
    main()
