# GBA.ODbLPolygon Building-Footprint Tile Index

[![License: ODbL](https://img.shields.io/badge/License-ODbL_1.0-blue.svg)](https://opendatacommons.org/licenses/odbl/1-0/)
[![Tiles](https://img.shields.io/badge/Tiles-922_Polygons-green.svg)](#tiles-per-region)
[![Total Dataset Size](https://img.shields.io/badge/Data_Size-~430_GB-orange.svg)](#tiles-per-region)
[![CRS](https://img.shields.io/badge/CRS-EPSG%3A4326-lightgrey.svg)](#attribute-table)
[![QGIS Plugin](https://img.shields.io/badge/QGIS_Plugin-gba__downloader-2b8a3e.svg)](#qgis-plugin-gba-building-footprint-downloader)
[![Release](https://img.shields.io/badge/Release-v1.0.0-informational.svg)](https://github.com/eqbalhassan/GBA-building-footprint-tile-index/releases)

A spatial index grid (ESRI Shapefile, GeoJSON, and CSV) with direct download URLs for the 922 five-degree ($5^\circ \times 5^\circ$) building-footprint tiles of the **GlobalBuildingAtlas `GBA.ODbLPolygon`** dataset hosted on Hugging Face.

The upstream Hugging Face repository stores hundreds of gigabytes of individual building footprints across seven continental folders without an interactive spatial index map. This repository fills that gap: load the index into **QGIS**, **ArcGIS Pro**, or **Python**, zoom to your study area, inspect the tile coverage and file size, and click or script the direct download link.

---

## Table of Contents

- [About the Dataset and Data Host](#about-the-dataset-and-data-host)
- [Repository Contents](#repository-contents)
- [QGIS Plugin: GBA Building Footprint Downloader](#qgis-plugin-gba-building-footprint-downloader)
- [Attribute Table Schema](#attribute-table-schema)
- [Tile Naming Convention](#tile-naming-convention)
- [Tiles Per Region](#tiles-per-region)
- [How to Use](#how-to-use)
  - [1. QGIS Plugin (Recommended)](#1-qgis-plugin-recommended)
  - [2. QGIS Manual Layer Action](#2-qgis-manual-layer-action)
  - [3. ArcGIS Pro](#3-arcgis-pro)
  - [4. Python (GeoPandas)](#4-python-geopandas)
  - [5. Command Line (cURL)](#5-command-line-curl)
- [Important Notes and Caveats](#important-notes-and-caveats)
- [How the Index Was Built and Regenerated](#how-the-index-was-built-and-regenerated)
- [License, Attribution, and Citation](#license-attribution-and-citation)
- [Maintainer](#maintainer)
- [Disclaimer](#disclaimer)

---

## About the Dataset and Data Host

- **Host Organization**: Hosted on Hugging Face under the organization [`zhu-xlab`](https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon), maintained by the **Chair of Data Science in Earth Observation** at the **Technical University of Munich (TUM)**, led by **Prof. Dr. Xiao Xiang Zhu**.
- **Dataset Repository**: [https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon](https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon)
- **Part of GlobalBuildingAtlas (GBA)**: GBA is an open, global, and complete dataset of individual building polygons (`GBA.Polygon`), building heights (`GBA.Height`), and Level of Detail 1 (LoD1) 3D building models (`GBA.LoD1`), providing consistent 2D and 3D architectural data at individual building scale worldwide.
- **Licensing Scope of this Subset**: This specific repository (`GBA.ODbLPolygon`) hosts **only** those building polygons that are distributed under the Open Database License (ODbL v1.0), sourced from **OpenStreetMap contributors** and **Microsoft GlobalML Building Footprints**.
- **Complete Dataset Archive**: The complete, unconstrained GlobalBuildingAtlas (including height estimations and 3D models) is archived on TUM's institutional repository **mediaTUM**: [https://mediatum.ub.tum.de/1782307](https://mediatum.ub.tum.de/1782307).
- **Code and Documentation**: [https://github.com/zhu-xlab/GlobalBuildingAtlas](https://github.com/zhu-xlab/GlobalBuildingAtlas)
- **Scientific Publication**: *GlobalBuildingAtlas: An Open Global and Complete Dataset of Building Polygons, Heights and LoD1 3D Models*, Earth System Science Data (ESSD), 2025. Preprint DOI: [10.5194/essd-2025-327](https://doi.org/10.5194/essd-2025-327); Final Journal DOI: [10.5194/essd-17-6647-2025](https://doi.org/10.5194/essd-17-6647-2025).
- **Hugging Face DOI**: [10.57967/hf/6771](https://doi.org/10.57967/hf/6771)
- **Structure**: Over **430 GB** (decompressed ~462 GB) structured into seven continental folders: `africa`, `asiaeast`, `asiawest`, `europe`, `northamerica`, `oceania`, and `southamerica`. Files are compressed GeoJSON formatted in $5^\circ \times 5^\circ$ geographic bounding boxes in EPSG:4326 (WGS 84).
- **Why this index is needed**: The Hugging Face dataset provides only raw nested directories. Without a spatial index, identifying which file corresponds to an Area of Interest (AOI) requires calculating bounding coordinates manually. This index allows immediate visual search and GIS integration.

---

## Repository Contents

```text
GBA-building-footprint-tile-index/
├── README.md                      # Comprehensive user documentation and usage workflows
├── LICENSE                        # Open Database License (ODbL) v1.0 Notice
├── NOTICE.md                      # Upstream data provenance and attribution
├── tile_index.csv                 # Flat tabular index with bounding coordinates
├── building_footprint/
│   ├── GBA_ODbLPolygon_grid.shp   # Main ESRI Shapefile polygon layer (EPSG:4326)
│   ├── GBA_ODbLPolygon_grid.shx   # Shapefile index
│   ├── GBA_ODbLPolygon_grid.dbf   # Attribute table
│   ├── GBA_ODbLPolygon_grid.prj   # WGS84 CRS definition
│   ├── GBA_ODbLPolygon_grid.cpg   # UTF-8 encoding declaration
│   └── GBA_ODbLPolygon_grid.geojson # Web-renderable GeoJSON map (renders on GitHub)
├── qgis_plugin/                   # Dedicated QGIS GUI Downloader Plugin
│   ├── gba_downloader.zip         # Ready-to-install plugin archive (Install from ZIP)
│   └── gba_downloader/            # Source plugin package (metadata, UI, QgsTask downloader)
├── docs/
│   ├── attribute_table.md         # Detailed field dictionary and dBASE specifications
│   └── tiles_per_region.md        # Per-continent statistics, sizes, and insights
└── scripts/
    ├── build_tile_index.py        # Automated, reproducible harvester and generator script
    └── requirements.txt           # Python script dependencies
```

---

## QGIS Plugin: GBA Building Footprint Downloader

This repository includes a dedicated, feature-packed QGIS plugin located in [`qgis_plugin/gba_downloader/`](qgis_plugin/gba_downloader/):

![Plugin Features](https://img.shields.io/badge/QGIS-3.16_to_3.99-green.svg)
![Multi-threaded](https://img.shields.io/badge/QgsTask-Non--blocking-blue.svg)

### Plugin Highlights:
1. **Built-in 5° × 5° Grid**: Instantly displays the global index grid on your QGIS map canvas styled with semi-transparent fills and tile name/size labels.
2. **Instant Spatial Queries**:
   - **Canvas Extent**: Queries and selects all tiles intersecting your current map view.
   - **Vector Layer Intersection**: Intersects any polygon vector layer in your project (e.g. city boundaries, district polygons, river basins) with the GBA grid.
   - **Interactive Selection**: Select tiles directly using QGIS's map canvas selection tool.
3. **Bandwidth & Storage Estimation**: Summarizes selected tile counts and total download sizes (in MB and GB), flagging empty tiles ($0\text{ MB}$) and huge files ($>1\text{ GB}$).
4. **Asynchronous Background Downloads (`QgsTask`)**: Downloads files on worker threads with live transfer speeds and progress bars without freezing QGIS.
5. **Automatic Layer Loading**: Automatically styles and loads downloaded GeoJSON footprints into your QGIS canvas under a dedicated `GlobalBuildingAtlas Footprints` layer group.

### Installing the Plugin:
- **Option A (Install from ZIP)**: In QGIS, open **Plugins** $\to$ **Manage and Install Plugins...** $\to$ **Install from ZIP**, select [`qgis_plugin/gba_downloader.zip`](qgis_plugin/gba_downloader.zip), and click **Install Plugin**.
- **Option B (Direct Profile Folder)**: Copy the `qgis_plugin/gba_downloader` folder into your QGIS plugins folder:
  - **Windows**: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
  - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
  - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

---

## Attribute Table Schema

The attribute table provides 4 core attributes designed for compatibility with GIS software:

| Field Name | Type | Width | Description |
| :--- | :--- | :--- | :--- |
| `region` | String | 15 | Continental directory name on Hugging Face (`africa`, `europe`, etc.) |
| `tile` | String | 30 | Unique $5^\circ \times 5^\circ$ tile identifier (e.g., `e000_n10_e005_n05`) |
| `size_mb` | Real | 12.3 | Remote GeoJSON file size in Megabytes (MB) |
| `url` | String | 254 | Permanent HTTPS download link to the building footprint GeoJSON |

*In `tile_index.csv`, bounding columns (`xmin`, `ymin`, `xmax`, `ymax`) are also provided.*

### Sample Rows (Preview)

| region | tile | size_mb | url |
| :--- | :--- | :--- | :--- |
| `africa` | `e000_n10_e005_n05` | `561.498` | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n10_e005_n05.geojson?download=true` |
| `africa` | `e000_n15_e005_n10` | `426.217` | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n15_e005_n10.geojson?download=true` |
| `africa` | `e000_n20_e005_n15` | `68.294` | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n20_e005_n15.geojson?download=true` |
| `africa` | `e000_n25_e005_n20` | `5.636` | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n25_e005_n20.geojson?download=true` |
| `africa` | `e000_n30_e005_n25` | `0.171` | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n30_e005_n25.geojson?download=true` |

For full field descriptions and dBase limits, see [docs/attribute_table.md](docs/attribute_table.md).

---

## Tile Naming Convention

Each tile spans exactly $5^\circ$ in longitude and $5^\circ$ in latitude, named according to its bounding corners:

$$\mathbf{\{e|w\}\{lon\_min\}\_\{n|s\}\{lat\_max\}\_\{e|w\}\{lon\_max\}\_\{n|s\}\{lat\_min\}}$$

### Worked Example: `e000_n10_e005_n05`
- `e000`: Minimum Longitude = $0^\circ\text{ E}$
- `n10`: Maximum Latitude = $10^\circ\text{ N}$
- `e005`: Maximum Longitude = $5^\circ\text{ E}$
- `n05`: Minimum Latitude = $5^\circ\text{ N}$

```text
               (lon_min, lat_max)                  (lon_max, lat_max)
                 (0° E, 10° N)                       (5° E, 10° N)
                       +-----------------------------------+
                       |                                   |
                       |                                   |
                       |       Tile: e000_n10_e005_n05     |
                       |       (5° x 5° bounding box)      |
                       |                                   |
                       |                                   |
                       +-----------------------------------+
                 (0° E, 5° N)                        (5° E, 5° N)
               (lon_min, lat_min)                  (lon_max, lat_min)
```

---

## Tiles Per Region

| Region | Tile Count | Total Size (MB) | Total Size (GB) | Largest Tile (MB) |
| :--- | :--- | :--- | :--- | :--- |
| **africa** | 176 | 63,769.91 | 62.28 GB | 3,084.00 MB |
| **asiaeast** | 128 | 29,677.51 | 28.98 GB | 9,744.08 MB |
| **asiawest** | 130 | 43,420.16 | 42.40 GB | 3,836.69 MB |
| **europe** | 94 | 182,329.88 | 178.06 GB | 13,539.19 MB |
| **northamerica** | 179 | 90,969.79 | 88.84 GB | 6,597.49 MB |
| **oceania** | 114 | 25,200.45 | 24.61 GB | 5,672.29 MB |
| **southamerica** | 101 | 5,273.93 | 5.15 GB | 311.63 MB |
| **TOTAL** | **922** | **440,641.63** | **430.31 GB** | **13,539.19 MB** |

For comprehensive notes on regional data density, see [docs/tiles_per_region.md](docs/tiles_per_region.md).

---

## How to Use

### 1. QGIS Plugin (Recommended)
1. Install and enable the **GBA Building Footprint Downloader** plugin in QGIS (see [above](#qgis-plugin-gba-building-footprint-downloader)).
2. Click the building footprint icon on your QGIS toolbar.
3. Click **"Show 5° Grid on Map"** to load the global index.
4. Zoom to your area of interest and click **"Intersect Current Map Extent"** (or use **"Intersect Active Layer"**).
5. Review the download size in the table and click **"Download Selected Tiles"**.
6. The building footprints will download in the background and appear automatically on your map!

### 2. QGIS Manual Layer Action
If you prefer not to use the plugin:
1. Drag and drop `building_footprint/GBA_ODbLPolygon_grid.shp` (or `.geojson`) into QGIS.
2. **Interactive Click-to-Download Action**:
   - Right-click layer $\to$ **Properties** $\to$ **Actions** tab.
   - Click the green **+** (Add Action) button.
   - Set **Type**: `Open URL`.
   - Set **Description**: `Download GeoJSON`.
   - Set **Action Text**: `[% "url" %]`.
   - Click **OK**.
   - Activate the **Run Feature Action** tool from the toolbar (or press `Ctrl+Shift+A`) and click any tile on the map to trigger immediate download in your default browser.
3. **Attribute Table**: Open the attribute table, select rows for your area, and copy the `url` column directly.

### 3. ArcGIS Pro
1. Add `GBA_ODbLPolygon_grid.shp` to an active Map.
2. Use **Select By Location** to select all tiles intersecting your project boundary or AOI.
3. Right-click layer $\to$ **Configure Pop-ups** $\to$ add a **Text / Hyperlink** pointing to `{url}`.
4. Alternatively, export the selected records' attribute table to CSV to queue batch downloads.

### 3. Python (GeoPandas)
Filter tiles intersecting a bounding box and download them with a streaming progress bar:

```python
import geopandas as gpd
import requests
import os

# Load the tile index
gdf = gpd.read_file("building_footprint/GBA_ODbLPolygon_grid.shp")

# Define your Area of Interest (e.g. minx, miny, maxx, maxy)
# Example: Northern Italy / Alps [6.5, 44.5, 12.5, 47.5]
aoi_box = (6.5, 44.5, 12.5, 47.5)
intersecting = gdf.cx[aoi_box[0]:aoi_box[2], aoi_box[1]:aoi_box[3]]

print(f"Found {len(intersecting)} tiles covering AOI:")
for idx, row in intersecting.iterrows():
    print(f" - {row['tile']} ({row['size_mb']} MB): {row['url']}")

# Download example
os.makedirs("downloads", exist_ok=True)
for _, row in intersecting.iterrows():
    dest = os.path.join("downloads", f"{row['tile']}.geojson")
    if os.path.exists(dest):
        continue
    print(f"Downloading {row['tile']} ({row['size_mb']} MB)...")
    with requests.get(row["url"], stream=True) as resp:
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
print("Downloads complete.")
```

### 4. Command Line (cURL)
To download an individual tile directly from terminal:

```bash
curl -L -o e000_n10_e005_n05.geojson "https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n10_e005_n05.geojson?download=true"
```
*(Always use `-L` or `--location` because Hugging Face resolve URLs issue an HTTP 302 redirect to their content delivery network).*

---

## Important Notes and Caveats

1. **Wide Variance in File Sizes**: Tile sizes range from a few bytes up to **13.5 GB**. Before downloading, always inspect the `size_mb` field to avoid unexpected disk saturation.
2. **Empty Tiles**: Some tiles in open oceans or desert fringes (e.g. `e010_n30_e015_n25`) contain 0 building features (`size_mb = 0.000 MB`). These are valid empty FeatureCollections.
3. **Redirects to Cloudflare CDN**: The permanent URLs stored in this index use Hugging Face's permanent resolve pattern (`.../resolve/main/...`). When requested, Hugging Face responds with an HTTP 302 redirect to a short-lived signed CDN URL. Always store and script against the permanent resolve URL, not the temporary signed CDN link.
4. **Tile Index Only**: This repository hosts **only the spatial index and boundary geometries**, not the heavy building-footprint GeoJSON datasets themselves.
5. **Upstream Updates**: If the authors update or add tiles on Hugging Face, run `scripts/build_tile_index.py` to regenerate the shapefile, GeoJSON, and CSV index.

---

## How the Index Was Built and Regenerated

The spatial index is built automatically via `scripts/build_tile_index.py`:
1. Queries the Hugging Face Tree REST API for all 7 regions with pagination (`limit=1000`, following `Link: <...>; rel="next"`).
2. Parses tile bounding coordinates using regex:
   `^([ew])(\d+)_([ns])(\d+)_([ew])(\d+)_([ns])(\d+)\.geojson$`
3. Converts coordinates to signed WGS84 floats and constructs rectangular polygon geometries.
4. Extracts file size in MB (`size_bytes / (1024 * 1024)`) and constructs permanent resolve URLs.
5. Exports to ESRI Shapefile, GeoJSON, and CSV.

To regenerate locally:
```bash
pip install -r scripts/requirements.txt
python scripts/build_tile_index.py --out building_footprint
```

---

## License, Attribution, and Citation

### License
- This index and the underlying building footprints are distributed under the **Open Database License (ODbL) v1.0**.
- See [LICENSE](LICENSE) for the full license notice and [NOTICE.md](NOTICE.md) for data provenance.

### Attribution
Contains data from **OpenStreetMap** (© OpenStreetMap contributors, ODbL) and **Microsoft Global ML Building Footprints**, processed and curated via **GlobalBuildingAtlas** (TUM Chair of Data Science in Earth Observation).

### Scientific Citation
If you use the GlobalBuildingAtlas building footprint data in research or publications, please cite the original authors:

```bibtex
@article{zhu2025globalbuildingatlas,
  title   = {GlobalBuildingAtlas: An Open Global and Complete Dataset of Building Polygons, Heights and LoD1 3D Models},
  author  = {Zhu, Xiao Xiang and Chen, Sining and Zhang, Fahong and Shi, Yilei and Wang, Yuanyuan},
  journal = {Earth System Science Data Discussions},
  volume  = {2025},
  pages   = {1--37},
  year    = {2025},
  doi     = {10.5194/essd-2025-327}
}
```

---

## Maintainer

Maintained by [@eqbalhassan](https://github.com/eqbalhassan).

---

## Disclaimer

This is an unofficial community-maintained spatial index. It is not affiliated with, endorsed by, or officially associated with the Technical University of Munich (TUM), Hugging Face, OpenStreetMap, or Microsoft.
