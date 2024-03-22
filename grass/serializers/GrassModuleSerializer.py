###############################################################################
# Filename: GrassModuleSerializer.py                                           #
# Project: OpenPlains Inc.                                                     #
# File Created: Sunday December 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Mar 22 2024                                               #
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
from .InputParameterSerializer import InputParameterSerializer
from .OutputParameterSerializer import OutputParameterSerializer
from .StdoutParserSerializer import StdoutParserSerializer


class GrassModuleSerializer(serializers.Serializer):
    """
    Serializer for GrassModule objects.

    The definition of a single GRASS GIS module and its inputs, outputs and flags. This module will be run in a location/mapset environment and is part of a process chain. The stdout and stderr output of modules that were run before this module in the process chain can be used as stdin for this module. The stdout of a module can be automatically transformed in list, table or key/value JSON representations in the HTTP response.

    Attributes:
        id (str): A unique id to identify the module call in the process chain to reference its stdout and stderr output as stdin in other modules..
        module (str): The name of the GRASS GIS module (r.univar, r.slope.aspect, v.select, ...) that should be executed. Use as module names &quot;importer&quot; or &quot;exporter&quot; to import or export raster layer, vector layer or other file based data without calling a GRASS GIS module.
        inputs (list[InputParameterSerializer], optional): List of input parameters for the GrassModule.
        outputs (list[OutputParameterSerializer], optional): List of output parameters for the GrassModule.
        flags (str, optional): Additional flags for the GrassModule.
        stdin (str, optional): Use the stdout output of a GRASS GIS module or executable of the process chain as input for this module. Refer to the module/executable output as id::stderr or id::stdout, the &quot;id&quot; is the unique identifier of a GRASS GIS module definition.
        stdout (StdoutParserSerializer, optional): Serializer for parsing the standard output of the GrassModule.
        overwrite (bool, optional): Flag indicating whether to overwrite existing files.
        verbose (bool, optional): Flag indicating whether to display verbose output.
        superquiet (bool, optional): Flag indicating whether to suppress all output.
        interface_description (bool, optional): Flag indicating whether to display the interface description of the GrassModule.
    """

    id = serializers.CharField(required=False)
    module = serializers.CharField(required=False)
    inputs = InputParameterSerializer(many=True, required=False)
    outputs = OutputParameterSerializer(many=True, required=False)
    flags = serializers.CharField(required=False)
    stdin = serializers.CharField(required=False)
    stdout = StdoutParserSerializer(required=False)
    overwrite = serializers.BooleanField(required=False)
    verbose = serializers.BooleanField(required=False)
    superquiet = serializers.BooleanField(required=False)
    interface_description = serializers.BooleanField(required=False)
