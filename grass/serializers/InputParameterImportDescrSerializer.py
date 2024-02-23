###############################################################################
# Filename: InputParameterImportDescrSerializer.py                             #
# Project: OpenPlains Inc.                                                     #
# File Created: Sunday December 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Sun Dec 17 2023                                               #
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

from rest_framework import serializers


class InputParameterImportDescrSerializer(serializers.Serializer):
    """
    Definition of sources to be imported as raster or vector map layer.

    Attributes:
    - type (str): The type of the input that should be downloaded and imported. In case of raster or vector types a download URL must be provided as source using http, https or ftp protocols. In case of sentinel2 scenes the scene name and the band must be provided. The Landsat approach is different. In case a Landsat scene is requested, all bands will be download, in the target location imported and an atmospheric correction is applied. The atmospheric correction must be specified. The resulting raster map layers have a specific name scheme, that is independent from the provided map name in the process description. The name scheme is always: <landsat scene id>_<atcor>.<band>. For example, if the scene LT52170762005240COA00 was requested, the resulting name for the DOS1 atmospheric corrected band 1 would be: LT52170762005240COA00_dos1.1. For the DOS1 atmospheric corrected band 2 it would be: LT52170762005240COA00_dos1.2 and so on. All other process steps must use these raster map layer names to refer to the imported Landsat bands. Use the file option to download any kind of files that should be processed by a grass gis module. [optional]
    - sentinel_band (str): The band of the sentinel2 scene that should be imported [optional]
    - landsat_atcor (str): The atmospheric correction that should be applied to the landsat scene [optional]
    - vector_layer (str): The name of the layer that should be imported from the vector file or postGIS database [optional]
    - source (str): The input source that may be a landsat scene name, a sentinel2 scene name, a postGIS database string, a stac collection ID or an URL that points to an accessible raster or vector file. A HTTP, HTTPS or FTP connection must be specified in case of raster or vector types. In this case the source string must contain the protocol that will used for connection: http:// or https:// or ftp://. PostGIS vector layer can be imported by defining a database string as source and a layer name. [optional]
    - semantic_label (str): Refers to the common names used to call the bands of an image, for example: red, blue, nir, swir. However, this property also accepts the band name such as B1, B8 etc. The semantic labeling should match the labels register in the stac collection. [optional]
    - extent (str): Spatio-temporal constraint defined by the user throughout bbox and interval concept. [optional]
    - filter (str): Constrain in any other property or metadata. [optional]
    - resample (str): Resampling method to use for reprojection of raster map (default: nearest). [optional]
    - resolution (str): Resolution of output raster map. Estimated, user-specified or current region resolution (default: estimated). [optional]
    - resolution_value (str): Resolution of output raster map (use with option "resolution": "value") in units of the target coordinate reference system, not in map units. Must be convertible to float. [optional]
    - basic_auth (str): User name and password for basic HTTP, HTTPS and FTP authentication of the source connection. The user name and password must be separated by a colon: username:password [optional]
    """

    type = serializers.CharField(required=False)
    sentinel_band = serializers.CharField(required=False)
    landsat_atcor = serializers.CharField(required=False)
    vector_layer = serializers.CharField(required=False)
    source = serializers.CharField(required=False)
    semantic_label = serializers.CharField(required=False)
    extent = serializers.CharField(required=False)
    filter = serializers.CharField(required=False)
    resample = serializers.CharField(required=False)
    resolution = serializers.CharField(required=False)
    resolution_value = serializers.CharField(required=False)
    basic_auth = serializers.CharField(required=False)
