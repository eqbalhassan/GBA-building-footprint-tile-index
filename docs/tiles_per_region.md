# Tiles Per Continental Region

This document breaks down the distribution of the 922 geographic tiles in the `GBA.ODbLPolygon` dataset across its seven continental directories on Hugging Face.

---

## 1. Summary Statistics Table

| Region (`region`) | Tile Count | Total Size (MB) | Total Size (GB) | Min Tile Size (MB) | Max Tile Size (MB) | Avg Tile Size (MB) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **africa** | 176 | 63,769.91 | 62.28 | 0.000 | 3,084.00 | 362.33 |
| **asiaeast** | 128 | 29,677.51 | 28.98 | 0.001 | 9,744.08 | 231.86 |
| **asiawest** | 130 | 43,420.16 | 42.40 | 0.003 | 3,836.69 | 334.00 |
| **europe** | 94 | 182,329.88 | 178.06 | 0.029 | 13,539.19 | 1,939.68 |
| **northamerica** | 179 | 90,969.79 | 88.84 | 0.002 | 6,597.49 | 508.21 |
| **oceania** | 114 | 25,200.45 | 24.61 | 0.000 | 5,672.29 | 221.06 |
| **southamerica** | 101 | 5,273.93 | 5.15 | 0.000 | 311.63 | 52.22 |
| **TOTAL** | **922** | **440,641.63** | **430.31** | **0.000** | **13,539.19** | **477.92** |

*(Note: 1 GB = 1,024 MB)*

---

## 2. Key Observations

1. **Europe Has the Highest Data Volume**: Despite having only 94 tiles (the fewest of any continent except South America), Europe represents over **178 GB (41.4%)** of the entire dataset. The average tile size in Europe is ~1.94 GB, reflecting the high density and completeness of OpenStreetMap building footprints across European nations.
2. **Dense Megacity Tiles**: The largest single tile is in Europe (`w005_n50_e000_n45.geojson`, covering parts of France and the UK) at **13.54 GB**, followed by a tile in East Asia (`e115_n40_e120_n35.geojson`, covering parts of Beijing/Hebei/Shandong) at **9.74 GB**.
3. **Empty / Oceanic Border Tiles**: Tiles with file sizes listed as `0.000` MB (e.g. `e010_n30_e015_n25.geojson` in Africa or `e150_s30_e155_s35.geojson` in Oceania) are valid 5° × 5° grid frames that happen to contain zero or negligible building footprints (often open desert or coastal waters). These files are only a few bytes in size (e.g., an empty GeoJSON FeatureCollection `{ "type": "FeatureCollection", "features": [] }`).
4. **Bandwidth Planning**: Users intending to download bulk continental tiles should check `size_mb` before queuing requests to avoid storage and network saturation.
