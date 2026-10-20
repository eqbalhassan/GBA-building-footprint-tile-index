# Attribute Table Field Dictionary

This document describes the schema and field definitions for the `GBA_ODbLPolygon_grid` shapefile and the accompanying `tile_index.csv` export.

---

## 1. Field Schema

| Field Name | Type | DBF Width / Decimals | CSV Header | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `region` | String | 15 / 0 | `region` | Continental folder name in the Hugging Face dataset repository (`zhu-xlab/GBA.ODbLPolygon`). | `africa` |
| `tile` | String | 30 / 0 | `tile` | Standard 5° × 5° tile identifier without file extension. Format: `{e\|w}{lon_min}_{n\|s}{lat_max}_{e\|w}{lon_max}_{n\|s}{lat_min}`. | `e000_n10_e005_n05` |
| `size_mb` | Real / Double | 12 / 3 | `size_mb` | File size of the corresponding building footprint GeoJSON file in Megabytes (MB). Computed from remote byte length. | `561.498` |
| `url` | String | 254 / 0 | `url` | Direct, permanent HTTPS download link to the GeoJSON file on Hugging Face (`?download=true`). | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n10_e005_n05.geojson?download=true` |
| `xmin` | Float | *N/A (Shape geometry)* | `xmin` | Westernmost longitude boundary of the tile in decimal degrees (EPSG:4326). Present in CSV export. | `0.0` |
| `ymin` | Float | *N/A (Shape geometry)* | `ymin` | Southernmost latitude boundary of the tile in decimal degrees (EPSG:4326). Present in CSV export. | `5.0` |
| `xmax` | Float | *N/A (Shape geometry)* | `xmax` | Easternmost longitude boundary of the tile in decimal degrees (EPSG:4326). Present in CSV export. | `5.0` |
| `ymax` | Float | *N/A (Shape geometry)* | `ymax` | Northernmost latitude boundary of the tile in decimal degrees (EPSG:4326). Present in CSV export. | `10.0` |

---

## 2. Sample Records (First 5 Rows)

| region | tile | size_mb | url | xmin | ymin | xmax | ymax |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `africa` | `e000_n10_e005_n05` | 561.498 | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n10_e005_n05.geojson?download=true` | 0.0 | 5.0 | 5.0 | 10.0 |
| `africa` | `e000_n15_e005_n10` | 426.217 | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n15_e005_n10.geojson?download=true` | 0.0 | 10.0 | 5.0 | 15.0 |
| `africa` | `e000_n20_e005_n15` | 68.294 | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n20_e005_n15.geojson?download=true` | 0.0 | 15.0 | 5.0 | 20.0 |
| `africa` | `e000_n25_e005_n20` | 5.636 | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n25_e005_n20.geojson?download=true` | 0.0 | 20.0 | 5.0 | 25.0 |
| `africa` | `e000_n30_e005_n25` | 0.171 | `https://huggingface.co/datasets/zhu-xlab/GBA.ODbLPolygon/resolve/main/africa/e000_n30_e005_n25.geojson?download=true` | 0.0 | 25.0 | 5.0 | 30.0 |

---

## 3. Shapefile & DBF Technical Specifications

- **ESRI Shapefile Field Name Limit**: In accordance with the dBase III specification, all shapefile field names are strictly $\le 10$ characters (`region`, `tile`, `size_mb`, `url`).
- **Maximum Character Width**: The `url` field is defined with a width of 254 bytes (the maximum allowable text field length in standard dBASE III). All current Hugging Face URLs in this dataset are between 110 and 125 characters, fitting comfortably without truncation.
- **Coordinate Reference System**: EPSG:4326 (WGS 84 geographic coordinate system; unprojected latitude/longitude in decimal degrees).
- **Encoding**: UTF-8 (specified in the companion `GBA_ODbLPolygon_grid.cpg` file).
