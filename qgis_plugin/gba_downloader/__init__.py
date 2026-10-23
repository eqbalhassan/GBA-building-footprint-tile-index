# -*- coding: utf-8 -*-
"""
GBA Building Footprint Downloader QGIS Plugin
Author: Eqbal Hassan
License: ODbL 1.0 / MIT
"""


def classFactory(iface):
    """Load GBABuildingFootprintPlugin class from file plugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .plugin import GBABuildingFootprintPlugin
    return GBABuildingFootprintPlugin(iface)
