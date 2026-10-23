# -*- coding: utf-8 -*-
"""
plugin.py
=========
Main QGIS Plugin class for GBA Building Footprint Downloader.
Integrates actions into QGIS Toolbar and Vector/Plugins Menus.
"""

import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon

from .downloader_dialog import GBADownloaderDialog


class GBABuildingFootprintPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.action = None
        self.dlg = None

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

        self.action = QAction(icon, "GBA Building Footprint Downloader", self.iface.mainWindow())
        self.action.setStatusTip("Download 5°x5° GlobalBuildingAtlas building footprints directly into QGIS")
        self.action.triggered.connect(self.run)

        # Add to Toolbar
        self.iface.addToolBarIcon(self.action)

        # Add to Vector Menu & Plugins Menu
        self.iface.addPluginToVectorMenu("GlobalBuildingAtlas", self.action)
        self.iface.addPluginToMenu("GlobalBuildingAtlas", self.action)

    def unload(self):
        """Removes the plugin menu items and icon from QGIS GUI."""
        if self.action:
            self.iface.removePluginVectorMenu("GlobalBuildingAtlas", self.action)
            self.iface.removePluginMenu("GlobalBuildingAtlas", self.action)
            self.iface.removeToolBarIcon(self.action)
            del self.action
            self.action = None

        if self.dlg:
            self.dlg.close()
            self.dlg = None

    def run(self):
        """Run method that performs all the real work."""
        if self.dlg is None:
            self.dlg = GBADownloaderDialog(self.iface, self.iface.mainWindow())

        self.dlg.show()
        self.dlg.raise_()
        self.dlg.activateWindow()
