# Social Media Announcements & Release Copy

This document contains ready-to-use social media copy for announcing the **GBA Building Footprint Tile Index & QGIS Plugin** on platforms such as Facebook, LinkedIn, and X (Twitter).

---

## 📘 Facebook Post

### Option 1: Story & Problem-Solver (Recommended for general audience)

```text
🌍 Tired of digging through massive 400+ GB datasets just to find building footprints for a single city?

Recently, the Chair of Data Science in Earth Observation at TUM (Technical University of Munich) released the GlobalBuildingAtlas (GBA.ODbLPolygon) on Hugging Face. It’s an incredible global dataset combining OpenStreetMap and Microsoft ML building footprints across 922 five-degree (5° x 5°) tiles.

🛑 The challenge:
There was no spatial index map. Finding which tile covered your study area meant manually calculating latitude/longitude coordinates and digging through nested directories. Worse, a single 5° tile can exceed 2.8 GB—often crashing your software if you only needed a small town!

💡 The solution:
I built and published an open-source Global Tile Index & QGIS Plugin to make this seamless:

🔹 Spatial Index Grid (Shapefile, GeoJSON & CSV): 922 polygons covering the globe with file sizes, coordinates, and direct download links.
🔹 Interactive QGIS Plugin (gba_downloader):
🎯 Draw AOI Rectangle: Simply drag a box directly on your QGIS map over your study area.
📊 Bandwidth Preview: Inspect download sizes before pulling data.
⚡ Auto-Spatial Clipping: Automatically extracts and plots ONLY the building footprints falling inside your study area!

💻 GitHub Repository:  
https://github.com/eqbalhassan/GBA-building-footprint-tile-index

You can install the plugin directly from the repo via ZIP. Feel free to star ⭐️ the project, try it out on your study area, and share your feedback!

#GIS #QGIS #RemoteSensing #Geospatial #OpenStreetMap #UrbanPlanning #BuildingFootprints #OpenSource #SpatialData
```

### Option 2: Feature-Focused & Direct (Great for GIS Groups)

```text
🚀 New Open-Source Release: GlobalBuildingAtlas QGIS Plugin & Tile Index!

If you work with building footprints, urban analytics, or disaster modeling, this tool will save you hours of work.

📦 What's included in the repository:
1️⃣ Global Tile Index (EPSG:4326): ESRI Shapefile, GeoJSON, and CSV index mapping all 922 tiles (~430 GB) of the Hugging Face GBA.ODbLPolygon dataset.
2️⃣ GBA Downloader QGIS Plugin (v1.1.0):
- Visual 5° × 5° grid layer directly on your canvas.
- "Draw AOI" interactive map tool to select your target zone.
- Multi-threaded background downloads (no QGIS UI freezing).
- In-memory spatial clipping: Reprojects and clips footprints strictly to your drawn boundary so you don't load gigabytes of unneeded polygons.

🔗 Explore & Download:  
https://github.com/eqbalhassan/GBA-building-footprint-tile-index

📹 Watch the attached 30-second walkthrough video to see it in action!

#QGIS #GIS #Geospatial #Python #DataEngineering #OpenData #Cartography
```

### Option 3: Short & Punchy

```text
🗺️ Extracting building footprints for any city in the world just got 10x easier!

I just released an open-source QGIS plugin & spatial index for the 430+ GB GlobalBuildingAtlas dataset. 

✅ Draw an AOI on your QGIS canvas  
✅ Preview file size  
✅ Download & auto-clip footprints strictly to your study area  

👉 Try it out here: https://github.com/eqbalhassan/GBA-building-footprint-tile-index

Check out the video below to see it in action! 👇

#GIS #QGIS #Geospatial #OpenStreetMap #UrbanPlanning
```

---

## 💼 LinkedIn Post

```text
Excited to share an open-source geospatial project: The GlobalBuildingAtlas (GBA) Tile Index & QGIS Downloader Plugin! 🌍🏢

The Technical University of Munich (TUM) Chair of Data Science in Earth Observation recently published GBA.ODbLPolygon on Hugging Face—a massive collection of building footprints worldwide combining OpenStreetMap and Microsoft GlobalML footprints.

To bridge the gap between large raw cloud datasets and practical GIS analysis, I developed:
1. A complete spatial index (Shapefile, GeoJSON, CSV) mapping all 922 5°x5° tiles with direct HTTPS download links and file size metadata.
2. A dedicated QGIS plugin (v1.1.0) featuring interactive AOI drawing on the map canvas and automated in-memory spatial clipping, enabling analysts to extract building footprints strictly for their study area without memory overload.

The project is fully open-source under ODbL 1.0. Check out the repository and video demo below!

🔗 GitHub: https://github.com/eqbalhassan/GBA-building-footprint-tile-index

#GIS #QGIS #Geospatial #RemoteSensing #DataEngineering #OpenSource #UrbanAnalytics #EarthObservation
```

---

## 🐦 X / Twitter Thread

```text
1/4 🌍 Working with global building footprints? The 430+ GB GBA.ODbLPolygon dataset hosted on Hugging Face now has an interactive QGIS plugin and spatial index!

Check it out: https://github.com/eqbalhassan/GBA-building-footprint-tile-index

2/4 🛑 The issue with large datasets: downloading multi-GB 5° tiles just to analyze a small study area freezes GIS software.
💡 Solution: The GBA Downloader plugin lets you draw an AOI on your map and automatically clips footprints to your bounding box in memory.

3/4 📦 Includes:
- 922-tile shapefile / GeoJSON / CSV index
- One-click install QGIS plugin
- Background non-blocking downloads via QgsTask
- Automated layer styling & zooming

4/4 ⭐️ Star the repo and test it on your study area:
https://github.com/eqbalhassan/GBA-building-footprint-tile-index
```
