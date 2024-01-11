###############################################################################
# Filename: DataTypeEnum.py                                                    #
# Project: OpenPlains Inc.                                                     #
# File Created: Wednesday December 27th 2023                                   #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Wed Dec 27 2023                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2023 OpenPlains Inc.                                           #
#                                                                              #
# django-actinia is an open-source django app that allows for with             #
# the Actinia REST API for GRASS GIS for distributed computational tasks.      #
#                                                                              #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with this program.  If not, see <https://www.gnu.org/licenses/>.       #
#                                                                              #
###############################################################################

from django.db import models
from django.utils.translation import gettext_lazy as _


class DataTypeEnum(models.TextChoices):
    """
    Enum class representing the different layer types.
    """

    TABULAR = "TA", _("tabular")
    CSV = "CS", _("csv")
    JSON = "JS", _("json")
    KML = "KM", _("kml")
    WMS = "WM", _("wms")
    WFS = "WF", _("wfs")
    PBF = "PB", _("pbf")
    GEOPACKAGE = "GP", _("geopackage")
    GEOTIFF = "GT", _("geotiff")
    NETCDF = "NC", _("netcdf")
    HDF5 = "HD", _("hdf5")
    HDF4 = "HF", _("hdf4")
    HDF = "H4", _("hdf")
    COG = "CG", _("cog")
    GEOJSON = "GJ", _("geojson")
    GEOPARQUET = "GQ", _("geoparquet")
    FLATGEOBUF = "FG", _("flatgeobuf")
    GPKG = "GK", _("gpkg")
    LAS = "LA", _("las")
    LAZ = "LZ", _("laz")
    XYZ = "XY", _("xyz")
    gltf = "GL", _("gltf")
    glb = "GB", _("glb")
    OBJ = "OB", _("obj")
