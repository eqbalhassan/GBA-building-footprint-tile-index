# GBA Building Footprint Downloader (QGIS Plugin)

A dedicated, lightweight QGIS plugin to visually explore, filter, and download $5^\circ \times 5^\circ$ building footprint tiles from the **GlobalBuildingAtlas `GBA.ODbLPolygon`** dataset directly into QGIS.

![Plugin Icon](icon.png)

---

## Features

- **Built-in 5° × 5° Global Grid**: One-click to visualize the global spatial index on your QGIS map canvas, styled with semi-transparent fills and tile name/size labels.
- **Spatial Extent Query**: Find and select tiles covering your current map canvas extent with a single click.
- **Layer Intersection Query**: Intersect any polygon vector layer in your QGIS project (e.g. study area boundary, municipal borders, river basins) with the GBA tile index.
- **Bandwidth & Storage Estimation**: Instant calculation of total download size and tile count, with color-coded warnings for large tiles (>1 GB) or empty ocean tiles.
- **Background Multi-Threaded Download (`QgsTask`)**: Downloads GeoJSON building footprints asynchronously without freezing the QGIS interface, displaying live transfer speeds and progress bars.
- **Automatic Project Loading**: Automatically loads downloaded GeoJSON footprints into your QGIS map canvas under a organized `GlobalBuildingAtlas Footprints` layer group.
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
1. Download `gba_downloader.zip` from the [GitHub Releases](https://github.com/eqbalhassan/GBA-building-footprint-tile-index/releases).
2. In QGIS, navigate to **Plugins** $\to$ **Manage and Install Plugins...**
3. Click **Install from ZIP** on the left panel.
4. Browse to `gba_downloader.zip` and click **Install Plugin**.

---

## How to Use

1. Click the **GBA Building Footprint Downloader** icon on the QGIS toolbar.
2. In the dialog:
   - Click **"Show 5° Grid on Map"** to see the global 922-tile coverage.
   - Navigate to your Area of Interest (AOI).
   - Click **"Intersect Current Map Extent"** or select a layer and click **"Intersect Active Layer"**.
   - Check the tiles you wish to download in the table.
   - Choose your destination download folder.
   - Click **"Download Selected Tiles"**.
3. Once downloaded, the building footprints will render automatically on your map!
