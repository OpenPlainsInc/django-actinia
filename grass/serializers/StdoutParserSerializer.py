###############################################################################
# Filename: StdoutParserSerializer.py                                          #
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


class StdoutParserSerializer(serializers.Serializer):
    """
    Use this parameter to automatically parse the output of GRASS GIS modules and convert the output into tables, lists or key/value pairs in the result section of the response.If the property type is set to table, list or kv then the stdout of the current command will be parsed and the result of the parse operation will be added to the result dictionary using the provided id as key. GRASS GIS modules produce regular output. Many modules have the flag -g to create key value pairs as stdout output. Other create a list of values or a table with/without header.

    Attributes:
        id (str): The unique id that is used to identify the parsed output in the result dictionary.
        format (str): The stdout format to be parsed.
        delimiter (str): The delimiter that should be used to parse table, list and key/value module output. Many GRASS GIS modules use by default &quot; NOTE: &quot; in tables and &quot;=&quot; in key/value pairs. A new line &quot;\n&quot; is always the delimiter between rows in the output.
    """

    id = serializers.CharField()
    format = serializers.CharField()
    delimiter = serializers.CharField()
