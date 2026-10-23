# -*- coding: utf-8 -*-
"""
downloader_dialog.py
====================
Interactive PyQt Dialog for GBA Building Footprint Downloader.
Handles spatial extent queries, layer intersection, tile selection,
and triggers asynchronous background downloads via QgsTask.
"""

import os
import json
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QCheckBox, QProgressBar, QGroupBox, QLineEdit, QComboBox,
    QMessageBox, QAbstractItemView, QFrame
)
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtGui import QColor, QFont, QIcon, QBrush
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsCoordinateTransform,
    QgsCoordinateReferenceSystem, QgsRectangle, QgsGeometry,
    QgsApplication, QgsSymbol, QgsSingleSymbolRenderer,
    QgsFillSymbol, QgsPalLayerSettings, QgsVectorLayerSimpleLabeling,
    QgsTextFormat, QgsTextBufferSettings
)

from .download_task import GBADownloadTask


class GBADownloaderDialog(QDialog):
    """
    Main interactive dialog for exploring and downloading GBA building footprints.
    """

    GRID_LAYER_NAME = "GlobalBuildingAtlas Tile Grid (5x5)"

    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.geojson_grid_path = os.path.join(self.plugin_dir, "data", "GBA_ODbLPolygon_grid.geojson")
        self.icon_path = os.path.join(self.plugin_dir, "icon.png")

        self.all_tiles = []        # All 922 tile records
        self.displayed_tiles = []  # Filtered/selected records in table
        self.active_task = None

        self.setWindowTitle("GlobalBuildingAtlas - Building Footprint Downloader")
        if os.path.exists(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path))

        self.resize(850, 700)
        self.load_grid_data()
        self.setup_ui()
        self.populate_table(self.all_tiles)

    def load_grid_data(self):
        """Loads tile index metadata from bundled GeoJSON."""
        if os.path.exists(self.geojson_grid_path):
            try:
                with open(self.geojson_grid_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for feat in data.get("features", []):
                        props = feat.get("properties", {})
                        geom = feat.get("geometry", {})
                        coords = geom.get("coordinates", [[]])[0]
                        if coords:
                            xs = [pt[0] for pt in coords]
                            ys = [pt[1] for pt in coords]
                            bbox = [min(xs), min(ys), max(xs), max(ys)]
                        else:
                            bbox = [0, 0, 0, 0]

                        props["bbox"] = bbox
                        self.all_tiles.append(props)
            except Exception as e:
                print(f"Error reading bundled GeoJSON: {e}")

    def setup_ui(self):
        """Constructs the dialog layout and widgets."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # 1. Header Banner
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px;")
        header_layout = QHBoxLayout(header_frame)

        if os.path.exists(self.icon_path):
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(self.icon_path).pixmap(48, 48))
            header_layout.addWidget(icon_label)

        title_layout = QVBoxLayout()
        title_lbl = QLabel("GlobalBuildingAtlas Building Footprints (GBA.ODbLPolygon)")
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title_lbl.setFont(title_font)
        title_lbl.setStyleSheet("color: #0F172A;")

        subtitle_lbl = QLabel("Browse, query, and download 5° × 5° building footprint tiles (OpenStreetMap & Microsoft ML) directly into QGIS.")
        subtitle_lbl.setStyleSheet("color: #475569; font-size: 11px;")
        title_layout.addWidget(title_lbl)
        title_layout.addWidget(subtitle_lbl)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        self.btn_load_grid = QPushButton("Show 5° Grid on Map")
        self.btn_load_grid.setStyleSheet("background-color: #0284C7; color: white; font-weight: bold; padding: 6px 12px; border-radius: 4px;")
        self.btn_load_grid.clicked.connect(self.load_grid_into_qgis)
        header_layout.addWidget(self.btn_load_grid)

        layout.addWidget(header_frame)

        # 2. Spatial Query & Filter Group
        query_group = QGroupBox("Spatial Query & Filter")
        query_layout = QVBoxLayout(query_group)

        btn_row = QHBoxLayout()
        self.btn_canvas_extent = QPushButton("Intersect Current Map Extent")
        self.btn_canvas_extent.clicked.connect(self.filter_by_canvas_extent)
        btn_row.addWidget(self.btn_canvas_extent)

        self.combo_layers = QComboBox()
        self.combo_layers.setMinimumWidth(180)
        self.refresh_vector_layers()
        btn_row.addWidget(self.combo_layers)

        self.btn_layer_intersect = QPushButton("Intersect Active Layer")
        self.btn_layer_intersect.clicked.connect(self.filter_by_layer)
        btn_row.addWidget(self.btn_layer_intersect)

        self.btn_sync_selection = QPushButton("Use Map Selection")
        self.btn_sync_selection.clicked.connect(self.sync_from_map_selection)
        btn_row.addWidget(self.btn_sync_selection)

        self.btn_reset_filter = QPushButton("Show All 922 Tiles")
        self.btn_reset_filter.clicked.connect(lambda: self.populate_table(self.all_tiles))
        btn_row.addWidget(self.btn_reset_filter)

        query_layout.addLayout(btn_row)

        # Quick text search row
        search_row = QHBoxLayout()
        search_lbl = QLabel("Filter text:")
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search by tile name (e.g. e000_n10) or region (e.g. europe)...")
        self.txt_search.textChanged.connect(self.filter_by_text)
        search_row.addWidget(search_lbl)
        search_row.addWidget(self.txt_search)

        self.btn_check_all = QPushButton("Check All")
        self.btn_check_all.clicked.connect(lambda: self.set_all_checked(True))
        self.btn_uncheck_all = QPushButton("Uncheck All")
        self.btn_uncheck_all.clicked.connect(lambda: self.set_all_checked(False))
        search_row.addWidget(self.btn_check_all)
        search_row.addWidget(self.btn_uncheck_all)

        query_layout.addLayout(search_row)
        layout.addWidget(query_group)

        # 3. Tiles Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Select", "Region", "Tile ID", "Size (MB)", "Bounding Box", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.itemChanged.connect(self.on_table_item_changed)
        layout.addWidget(self.table)

        # 4. Output Settings Group
        settings_group = QGroupBox("Download Settings")
        settings_layout = QVBoxLayout(settings_group)

        dir_row = QHBoxLayout()
        dir_lbl = QLabel("Save Folder:")
        self.txt_dir = QLineEdit()
        saved_dir = QSettings().value("GBADownloader/download_dir", os.path.join(os.path.expanduser("~"), "Downloads", "GBA_Building_Footprints"))
        self.txt_dir.setText(saved_dir)

        self.btn_browse = QPushButton("Browse...")
        self.btn_browse.clicked.connect(self.browse_download_dir)
        dir_row.addWidget(dir_lbl)
        dir_row.addWidget(self.txt_dir)
        dir_row.addWidget(self.btn_browse)
        settings_layout.addLayout(dir_row)

        opts_row = QHBoxLayout()
        self.chk_auto_load = QCheckBox("Automatically add downloaded GeoJSON footprints to project canvas")
        self.chk_auto_load.setChecked(True)
        self.chk_skip_existing = QCheckBox("Skip files that already exist on disk")
        self.chk_skip_existing.setChecked(True)
        opts_row.addWidget(self.chk_auto_load)
        opts_row.addWidget(self.chk_skip_existing)
        opts_row.addStretch()
        settings_layout.addLayout(opts_row)

        layout.addWidget(settings_group)

        # 5. Progress and Summary Row
        summary_frame = QFrame()
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setContentsMargins(0, 0, 0, 0)

        self.lbl_summary = QLabel("Selected: 0 tiles | Total Size: 0.0 MB")
        self.lbl_summary.setStyleSheet("font-weight: bold; color: #1E293B; font-size: 12px;")
        summary_layout.addWidget(self.lbl_summary)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        summary_layout.addWidget(self.progress_bar)

        self.lbl_status = QLabel("Ready")
        self.lbl_status.setStyleSheet("color: #64748B; font-size: 11px;")
        summary_layout.addWidget(self.lbl_status)

        layout.addWidget(summary_frame)

        # 6. Action Buttons
        btn_action_layout = QHBoxLayout()
        btn_action_layout.addStretch()

        self.btn_download = QPushButton("Download Selected Tiles")
        self.btn_download.setStyleSheet(
            "background-color: #10B981; color: white; font-weight: bold; font-size: 12px; padding: 8px 20px; border-radius: 4px;"
        )
        self.btn_download.clicked.connect(self.start_download)
        btn_action_layout.addWidget(self.btn_download)

        self.btn_cancel = QPushButton("Cancel Download")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self.cancel_download)
        btn_action_layout.addWidget(self.btn_cancel)

        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.close)
        btn_action_layout.addWidget(self.btn_close)

        layout.addLayout(btn_action_layout)

    def refresh_vector_layers(self):
        """Populates the combo box with polygon vector layers in the project."""
        self.combo_layers.clear()
        self.combo_layers.addItem("-- Select Project Layer --", None)
        project = QgsProject.instance()
        for layer_id, layer in project.mapLayers().items():
            if isinstance(layer, QgsVectorLayer) and layer.geometryType() == 2:  # Polygon
                self.combo_layers.addItem(layer.name(), layer)

    def populate_table(self, tiles):
        """Fills the table widget with tile items."""
        self.displayed_tiles = tiles
        self.table.blockSignals(True)
        self.table.setRowCount(len(tiles))

        for row_idx, item in enumerate(tiles):
            # 0: Checkbox
            chk_item = QTableWidgetItem()
            chk_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chk_item.setCheckState(Qt.Checked if len(tiles) <= 20 else Qt.Unchecked)
            self.table.setItem(row_idx, chk_item)

            # 1: Region
            reg_item = QTableWidgetItem(item.get("region", ""))
            reg_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(row_idx, reg_item)

            # 2: Tile Name
            tile_name = item.get("tile", "")
            name_item = QTableWidgetItem(tile_name)
            name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(row_idx, name_item)

            # 3: Size (MB)
            size_mb = float(item.get("size_mb", 0.0))
            size_item = QTableWidgetItem(f"{size_mb:,.1f}")
            size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            size_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            if size_mb > 1000.0:
                size_item.setForeground(QBrush(QColor("#E11D48")))  # Red for >1 GB
            elif size_mb > 200.0:
                size_item.setForeground(QBrush(QColor("#D97706")))  # Amber for >200 MB
            self.table.setItem(row_idx, size_item)

            # 4: Bounding Box
            bbox = item.get("bbox", [0, 0, 0, 0])
            bbox_str = f"[{bbox[0]:.1f}, {bbox[1]:.1f}, {bbox[2]:.1f}, {bbox[3]:.1f}]"
            bbox_item = QTableWidgetItem(bbox_str)
            bbox_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(row_idx, bbox_item)

            # 5: Status
            status_item = QTableWidgetItem("Ready")
            status_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(row_idx, status_item)

        self.table.blockSignals(False)
        self.update_summary()

    def set_all_checked(self, checked_state):
        """Checks or unchecks all rows currently visible in the table."""
        self.table.blockSignals(True)
        state = Qt.Checked if checked_state else Qt.Unchecked
        for r in range(self.table.rowCount()):
            item = self.table.item(r, 0)
            if item:
                item.setCheckState(state)
        self.table.blockSignals(False)
        self.update_summary()

    def on_table_item_changed(self, item):
        if item.column() == 0:
            self.update_summary()

    def update_summary(self):
        """Calculates total selected tiles and total file size."""
        selected_count = 0
        total_size_mb = 0.0

        for r in range(self.table.rowCount()):
            chk_item = self.table.item(r, 0)
            if chk_item and chk_item.checkState() == Qt.Checked:
                selected_count += 1
                size_item = self.table.item(r, 3)
                if size_item:
                    try:
                        total_size_mb += float(size_item.text().replace(",", ""))
                    except ValueError:
                        pass

        if total_size_mb >= 1024.0:
            size_str = f"{total_size_mb:,.1f} MB ({(total_size_mb / 1024.0):.2f} GB)"
        else:
            size_str = f"{total_size_mb:,.1f} MB"

        self.lbl_summary.setText(f"Selected: {selected_count} tiles | Total Size: {size_str}")

    def filter_by_text(self, text):
        """Filters table by substring matching tile ID or region."""
        query = text.strip().lower()
        if not query:
            filtered = self.all_tiles
        else:
            filtered = [
                t for t in self.all_tiles
                if query in t.get("tile", "").lower() or query in t.get("region", "").lower()
            ]
        self.populate_table(filtered)

    def load_grid_into_qgis(self):
        """Adds the GBA 5°x5° index GeoJSON to the QGIS map canvas."""
        project = QgsProject.instance()
        existing = project.mapLayersByName(self.GRID_LAYER_NAME)
        if existing:
            self.iface.setActiveLayer(existing[0])
            self.iface.messageBar().pushInfo("GBA Downloader", "GBA Tile Grid layer is already in project.")
            return existing[0]

        layer = QgsVectorLayer(self.geojson_grid_path, self.GRID_LAYER_NAME, "ogr")
        if not layer.isValid():
            QMessageBox.critical(self, "Error", "Could not load bundled GBA Tile Grid GeoJSON.")
            return None

        # Clean style: transparent fill with distinct blue border
        sym = QgsFillSymbol.createSimple({
            "color": "0,168,255,30",
            "outline_color": "#0284C7",
            "outline_width": "0.8"
        })
        layer.setRenderer(QgsSingleSymbolRenderer(sym))

        # Add rule-based labeling showing tile and size
        pal = QgsPalLayerSettings()
        pal.fieldName = "tile || '\n(' || round(size_mb, 1) || ' MB)'"
        pal.placement = QgsPalLayerSettings.OverPoint
        txt_fmt = QgsTextFormat()
        txt_fmt.setSize(7.5)
        txt_fmt.setColor(QColor("#0F172A"))
        buf = QgsTextBufferSettings()
        buf.setEnabled(True)
        buf.setSize(1.0)
        buf.setColor(QColor(255, 255, 255, 220))
        txt_fmt.setBuffer(buf)
        pal.setFormat(txt_fmt)
        layer.setLabeling(QgsVectorLayerSimpleLabeling(pal))
        layer.setLabelsEnabled(True)

        project.addMapLayer(layer)
        self.iface.setActiveLayer(layer)
        self.iface.messageBar().pushSuccess("GBA Downloader", "Added GBA 5°x5° Tile Grid layer to map.")
        return layer

    def filter_by_canvas_extent(self):
        """Finds all tiles that intersect current canvas extent in EPSG:4326."""
        canvas = self.iface.mapCanvas()
        extent = canvas.extent()
        src_crs = canvas.mapSettings().destinationCrs()
        tgt_crs = QgsCoordinateReferenceSystem("EPSG:4326")

        if src_crs != tgt_crs:
            transform = QgsCoordinateTransform(src_crs, tgt_crs, QgsProject.instance())
            extent_4326 = transform.transformBoundingBox(extent)
        else:
            extent_4326 = extent

        geom_extent = QgsGeometry.fromRect(extent_4326)

        intersecting = []
        for t in self.all_tiles:
            b = t.get("bbox", [0, 0, 0, 0])
            tile_rect = QgsRectangle(b[0], b[1], b[2], b[3])
            tile_geom = QgsGeometry.fromRect(tile_rect)
            if geom_extent.intersects(tile_geom):
                intersecting.append(t)

        self.populate_table(intersecting)
        self.set_all_checked(True)
        self.iface.messageBar().pushInfo("GBA Downloader", f"Found {len(intersecting)} tiles intersecting map canvas.")

    def filter_by_layer(self):
        """Intersects GBA tiles with the polygon layer selected in the dropdown."""
        layer = self.combo_layers.currentData()
        if not layer or not layer.isValid():
            QMessageBox.warning(self, "Select Layer", "Please select a valid vector layer from the dropdown.")
            return

        tgt_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        transform = QgsCoordinateTransform(layer.crs(), tgt_crs, QgsProject.instance()) if layer.crs() != tgt_crs else None

        # Build union geometry of selected or all features
        geoms = []
        features = layer.selectedFeatures() if layer.selectedFeatureCount() > 0 else layer.getFeatures()
        for f in features:
            if f.hasGeometry():
                g = QgsGeometry(f.geometry())
                if transform:
                    g.transform(transform)
                geoms.append(g)

        if not geoms:
            QMessageBox.warning(self, "No Geometry", "Selected layer has no valid polygon geometries.")
            return

        combined_geom = QgsGeometry.unaryUnion(geoms)

        intersecting = []
        for t in self.all_tiles:
            b = t.get("bbox", [0, 0, 0, 0])
            tile_rect = QgsRectangle(b[0], b[1], b[2], b[3])
            tile_geom = QgsGeometry.fromRect(tile_rect)
            if combined_geom.intersects(tile_geom):
                intersecting.append(t)

        self.populate_table(intersecting)
        self.set_all_checked(True)
        self.iface.messageBar().pushInfo("GBA Downloader", f"Found {len(intersecting)} tiles intersecting layer '{layer.name()}'.")

    def sync_from_map_selection(self):
        """Pulls selection directly from the GBA Tile Grid layer in QGIS."""
        project = QgsProject.instance()
        layers = project.mapLayersByName(self.GRID_LAYER_NAME)
        if not layers:
            QMessageBox.information(self, "Grid Layer", "GBA Tile Grid layer is not loaded in project. Click 'Show 5° Grid on Map' first.")
            return

        grid_layer = layers[0]
        selected_feats = grid_layer.selectedFeatures()
        if not selected_feats:
            QMessageBox.information(self, "No Selection", "No features are currently selected on the GBA Grid layer.")
            return

        selected_tile_names = {f["tile"] for f in selected_feats if "tile" in f.fields().names()}
        matching = [t for t in self.all_tiles if t.get("tile") in selected_tile_names]
        self.populate_table(matching)
        self.set_all_checked(True)

    def browse_download_dir(self):
        """Opens folder dialog to choose download target directory."""
        current = self.txt_dir.text()
        chosen = QFileDialog.getExistingDirectory(self, "Select Download Directory", current)
        if chosen:
            self.txt_dir.setText(chosen)
            QSettings().setValue("GBADownloader/download_dir", chosen)

    def start_download(self):
        """Gathers selected tiles and initiates background download task."""
        selected_items = []
        for r in range(self.table.rowCount()):
            chk = self.table.item(r, 0)
            if chk and chk.checkState() == Qt.Checked:
                tile_id = self.table.item(r, 2).text()
                # Find tile dict
                match = next((t for t in self.displayed_tiles if t.get("tile") == tile_id), None)
                if match:
                    selected_items.append(match)

        if not selected_items:
            QMessageBox.warning(self, "No Tiles Selected", "Please check at least one tile to download.")
            return

        download_dir = self.txt_dir.text().strip()
        if not download_dir:
            QMessageBox.warning(self, "Invalid Directory", "Please choose a valid download folder.")
            return

        # Warning for huge downloads
        total_mb = sum(float(x.get("size_mb", 0.0)) for x in selected_items)
        if total_mb > 3000.0:
            resp = QMessageBox.question(
                self,
                "Large Download Warning",
                f"You have selected {len(selected_items)} tiles totaling {total_mb/1024.0:.2f} GB.\n"
                "This download may take considerable time and bandwidth. Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if resp != QMessageBox.Yes:
                return

        # Prepare UI
        self.btn_download.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.lbl_status.setText("Initializing download task...")

        skip_existing = self.chk_skip_existing.isChecked()
        self.active_task = GBADownloadTask(selected_items, download_dir, skip_existing)

        self.active_task.tileStarted.connect(self.on_tile_started)
        self.active_task.tileProgress.connect(self.on_tile_progress)
        self.active_task.tileCompleted.connect(self.on_tile_completed)
        self.active_task.overallProgress.connect(self.on_overall_progress)
        self.active_task.taskCompleted.connect(self.on_download_finished)
        self.active_task.taskTerminated.connect(self.on_download_canceled)

        QgsApplication.taskManager().addTask(self.active_task)

    def cancel_download(self):
        """Cancels running task."""
        if self.active_task:
            self.lbl_status.setText("Canceling downloads...")
            self.active_task.cancel()
            self.btn_cancel.setEnabled(False)

    def on_tile_started(self, tile_name, size_mb):
        self.lbl_status.setText(f"Downloading {tile_name} ({size_mb:.1f} MB)...")
        # Update table status
        for r in range(self.table.rowCount()):
            if self.table.item(r, 2).text() == tile_name:
                self.table.item(r, 5).setText("Downloading...")
                self.table.item(r, 5).setForeground(QBrush(QColor("#0284C7")))
                break

    def on_tile_progress(self, tile_name, pct, downloaded_bytes, total_bytes, speed_kbps):
        speed_str = f"{speed_kbps/1024.0:.1f} MB/s" if speed_kbps >= 1024.0 else f"{speed_kbps:.0f} KB/s"
        self.lbl_status.setText(f"Downloading {tile_name}: {pct}% ({speed_str})")

    def on_tile_completed(self, tile_name, local_path, success, error_msg):
        for r in range(self.table.rowCount()):
            if self.table.item(r, 2).text() == tile_name:
                status_item = self.table.item(r, 5)
                if success:
                    status_item.setText("Completed")
                    status_item.setForeground(QBrush(QColor("#10B981")))  # Green
                    if self.chk_auto_load.isChecked() and os.path.exists(local_path):
                        self.load_geojson_layer(tile_name, local_path)
                else:
                    status_item.setText(f"Failed: {error_msg}")
                    status_item.setForeground(QBrush(QColor("#EF4444")))  # Red
                break

    def on_overall_progress(self, completed_count, total_count):
        pct = int((completed_count / total_count) * 100) if total_count > 0 else 0
        self.progress_bar.setValue(pct)

    def load_geojson_layer(self, tile_name, local_path):
        """Loads downloaded GeoJSON footprints into the project under a dedicated group."""
        project = QgsProject.instance()
        group_name = "GlobalBuildingAtlas Footprints"
        root = project.layerTreeRoot()
        group = root.findGroup(group_name)
        if not group:
            group = root.addGroup(group_name)

        layer_name = f"GBA_{tile_name}"
        layer = QgsVectorLayer(local_path, layer_name, "ogr")
        if layer.isValid():
            # Style buildings nicely: warm gray polygon with fine dark outline
            sym = QgsFillSymbol.createSimple({
                "color": "#CBD5E1",
                "outline_color": "#475569",
                "outline_width": "0.4"
            })
            layer.setRenderer(QgsSingleSymbolRenderer(sym))
            project.addMapLayer(layer, False)
            group.addLayer(layer)

    def on_download_finished(self):
        self.btn_download.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.lbl_status.setText("All downloads finished!")
        self.iface.messageBar().pushSuccess("GBA Downloader", "Building footprints downloaded successfully.")

    def on_download_canceled(self):
        self.btn_download.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.lbl_status.setText("Download canceled by user.")
        self.iface.messageBar().pushWarning("GBA Downloader", "Download task was canceled.")
