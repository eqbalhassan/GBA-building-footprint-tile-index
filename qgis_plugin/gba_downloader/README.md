# GBA Building Footprint Downloader (QGIS Plugin)

A dedicated, lightweight QGIS plugin to visually explore, filter, and download $5^\circ \times 5^\circ$ building footprint tiles from the **GlobalBuildingAtlas `GBA.ODbLPolygon`** dataset directly into QGIS.

![Plugin Icon](icon.png)

---

## Features

- **🎯 Interactive AOI Drawing Tool**: Click **"Draw AOI Rectangle on Canvas"** to drag and define your exact study area directly on the map.
- **⚡ Automatic Spatial AOI Clipping**: When downloading large 5° × 5° tiles (often 500 MB–2.8 GB), the plugin automatically reprojects and extracts only the building footprints within your defined study area rectangle, saving memory and keeping your QGIS canvas fast.
- **Built-in 5° × 5° Global Grid**: One-click to visualize the global spatial index on your QGIS map canvas, styled with semi-transparent fills and tile name/size labels.
- **Spatial Extent Query**: Find and select tiles covering your current map canvas extent with a single click.
- **Layer Intersection Query**: Intersect any polygon vector layer in your QGIS project (e.g. study area boundary, municipal borders, river basins) with the GBA tile index.
- **Bandwidth & Storage Estimation**: Instant calculation of total download size and tile count, with color-coded warnings for large tiles (>1 GB) or empty ocean tiles.
- **Background Multi-Threaded Download (`QgsTask`)**: Downloads GeoJSON building footprints asynchronously without freezing the QGIS interface, displaying live transfer speeds and progress bars.
- **Automatic Project Loading & Styling**: Automatically loads extracted footprints into your QGIS map canvas styled in a dedicated `GlobalBuildingAtlas Footprints` layer group and zooms to fit.
- **Skip Existing Files**: Avoids re-downloading files already saved in your local folder.

---

## Installation

### Method 1: Automatic / Direct Profile Install (Already Installed on this machine)
The plugin is located directly in your QGIS plugin directory:
`%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\gba_downloader`

To activate:
1. Open **QGIS**.
2. Go to **Plugins** $\to$ **Manage and Install Plugins...**
3. Select **Installed** on the left panel.
4. Check the box next to **GBA Building Footprint Downloader**.
5. The building icon will appear in your top toolbar and in the **Vector** $\to$ **GlobalBuildingAtlas** menu!

### Method 2: Install from ZIP file
1. Download `gba_downloader.zip` from this repository or the [GitHub Releases](https://github.com/eqbalhassan/GBA-building-footprint-tile-index/releases).
2. In QGIS, navigate to **Plugins** $\to$ **Manage and Install Plugins...**
3. Click **Install from ZIP** on the left panel.
4. Browse to `gba_downloader.zip` and click **Install Plugin**.

---

## How to Use

1. Click the **GBA Building Footprint Downloader** icon on the QGIS toolbar.
2. In the dialog:
   - Click **"🎯 Draw AOI Rectangle on Canvas"** and drag a bounding box over your study area (or use **"Intersect Current View Extent"**).
   - The plugin automatically checks intersecting tiles and displays their sizes.
   - Keep **"Clip downloaded building footprints to AOI rectangle"** checked to extract only the buildings inside your study area.
   - Choose your destination download folder.
   - Click **"Download & Plot Building Footprints"**.
3. The plugin downloads the tile in the background, extracts the building polygons for your AOI, styles them, and zooms the canvas right to your study area!
