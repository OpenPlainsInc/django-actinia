###############################################################################
# Filename: OputParameterSerializer.py                                         #
# Project: OpenPlains Inc.                                                     #
# File Created: Sunday December 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Thu Jan 11 2024                                               #
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
from .OutputParameterMetadataSerializer import OutputParameterMetadataSerializer
from .OutputParameterExportSerializer import OutputParameterExportSerializer


class OutputParameterSerializer(serializers.Serializer):
    """
    Serializer for output parameters.

    Attributes:
        param (str): The name of a GRASS GIS module parameter like map or elevation.
        value (str): The value of the GRASS GIS module parameter. Raster, vector and STDS inputs must contain the mapset name in their id: slope@PERMANENT, if they are not located in the working mapset. Do not contain the mapset name in map names that are processed, since the mapsets are generated on demand using random names. Outputs are not allowed to contain mapset names.Files that are created in the process chain to exchange data can be specified using the $file::unique_id identifier. The unique_id will be replaced with a temporary file name, that is available in the whole process chain at runtime. The unique_id is the identifier that can be used by different modules in a process chain to access the same temporary file or to prepare it for export.
        export (OutputParameterExportSerializer, optional): Serializer for export information (default: None).
        metadata (OutputParameterMetadataSerializer, optional): Serializer for metadata information (default: None).
    """

    param = serializers.CharField()
    value = serializers.CharField()
    export = OutputParameterExportSerializer(required=False)
    metadata = OutputParameterMetadataSerializer(required=False)
