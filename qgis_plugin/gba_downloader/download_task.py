# -*- coding: utf-8 -*-
"""
download_task.py
================
Asynchronous background download task using QgsTask for non-blocking downloads
of large GBA building-footprint GeoJSON tiles into QGIS.
"""

import os
import time
import urllib.request
import urllib.error
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsTask, QgsMessageLog, Qgis


class GBADownloadTask(QgsTask):
    """
    QgsTask worker that downloads a list of GBA GeoJSON tiles in the background,
    reporting progress and notifying when each file finishes.
    """

    # Signals:
    # tileStarted(tile_name, size_mb)
    tileStarted = pyqtSignal(str, float)
    # tileProgress(tile_name, percent_int, bytes_downloaded, total_bytes, speed_kbps)
    tileProgress = pyqtSignal(str, int, int, int, float)
    # tileCompleted(tile_name, local_path, success, error_message)
    tileCompleted = pyqtSignal(str, str, bool, str)
    # overallProgress(completed_count, total_count)
    overallProgress = pyqtSignal(int, int)

    def __init__(self, tiles, download_dir, skip_existing=True):
        description = f"Downloading {len(tiles)} GlobalBuildingAtlas Tile(s)"
        super().__init__(description, QgsTask.CanCancel)
        self.tiles = tiles  # list of dicts: {'region', 'tile', 'size_mb', 'url', ...}
        self.download_dir = download_dir
        self.skip_existing = skip_existing
        self.completed_count = 0
        self.total_count = len(tiles)
        self.downloaded_paths = []

    def run(self):
        """
        Main worker execution loop running in a background thread.
        """
        QgsMessageLog.logMessage(
            f"Starting download task for {self.total_count} tiles into {self.download_dir}",
            "GBADownloader",
            Qgis.Info
        )

        os.makedirs(self.download_dir, exist_ok=True)

        for i, item in enumerate(self.tiles):
            if self.isCanceled():
                QgsMessageLog.logMessage("Download task was canceled by user.", "GBADownloader", Qgis.Warning)
                return False

            tile_name = item.get("tile", "unknown")
            region = item.get("region", "")
            url = item.get("url", "")
            size_mb = float(item.get("size_mb", 0.0))

            dest_filename = f"{tile_name}.geojson"
            dest_path = os.path.join(self.download_dir, dest_filename)
            part_path = f"{dest_path}.part"

            self.tileStarted.emit(tile_name, size_mb)

            # Check if file already exists and is valid
            if self.skip_existing and os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
                QgsMessageLog.logMessage(f"Tile {tile_name} already exists. Skipping download.", "GBADownloader", Qgis.Info)
                self.completed_count += 1
                self.downloaded_paths.append(dest_path)
                self.tileCompleted.emit(tile_name, dest_path, True, "Already exists")
                self.overallProgress.emit(self.completed_count, self.total_count)
                self.setProgress((self.completed_count / self.total_count) * 100.0)
                continue

            # Download using streaming HTTP
            success = False
            error_msg = ""
            try:
                headers = {
                    "User-Agent": "QGIS-GBA-Footprint-Downloader/1.0 (+https://github.com/eqbalhassan/GBA-building-footprint-tile-index)"
                }
                req = urllib.request.Request(url, headers=headers)

                start_time = time.time()
                last_update_time = start_time
                downloaded_bytes = 0

                with urllib.request.urlopen(req, timeout=30) as response, open(part_path, "wb") as out_file:
                    total_bytes = int(response.headers.get("Content-Length", 0))
                    if total_bytes <= 0 and size_mb > 0:
                        total_bytes = int(size_mb * 1024 * 1024)

                    chunk_size = 1024 * 64  # 64 KB chunks
                    while True:
                        if self.isCanceled():
                            out_file.close()
                            if os.path.exists(part_path):
                                os.remove(part_path)
                            return False

                        chunk = response.read(chunk_size)
                        if not chunk:
                            break

                        out_file.write(chunk)
                        downloaded_bytes += len(chunk)

                        now = time.time()
                        if now - last_update_time >= 0.2:  # throttled UI signal updates
                            elapsed = max(now - start_time, 0.001)
                            speed_kbps = (downloaded_bytes / 1024.0) / elapsed
                            pct = int((downloaded_bytes / total_bytes) * 100) if total_bytes > 0 else 0
                            pct = min(max(pct, 0), 100)
                            self.tileProgress.emit(tile_name, pct, downloaded_bytes, total_bytes, speed_kbps)
                            last_update_time = now

                # Download complete: rename .part to final destination
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                os.rename(part_path, dest_path)
                success = True
                self.downloaded_paths.append(dest_path)

            except urllib.error.URLError as e:
                error_msg = f"Network error: {e.reason}"
            except Exception as e:
                error_msg = f"Download error: {str(e)}"
            finally:
                if not success and os.path.exists(part_path):
                    try:
                        os.remove(part_path)
                    except OSError:
                        pass

            self.completed_count += 1
            self.overallProgress.emit(self.completed_count, self.total_count)
            self.setProgress((self.completed_count / self.total_count) * 100.0)
            self.tileCompleted.emit(tile_name, dest_path, success, error_msg)

        return True

    def finished(self, result):
        """
        Executed on the main QGIS GUI thread once all downloads conclude.
        """
        if result:
            QgsMessageLog.logMessage(
                f"GBA Download Task completed. {len(self.downloaded_paths)} tiles downloaded.",
                "GBADownloader",
                Qgis.Success
            )
        else:
            QgsMessageLog.logMessage(
                "GBA Download Task halted or canceled.",
                "GBADownloader",
                Qgis.Warning
            )
