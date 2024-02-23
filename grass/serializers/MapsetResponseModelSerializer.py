###############################################################################
# Filename: MapsetResponseSerializer.py                                        #
# Project: OpenPlains Inc.                                                     #
# File Created: Thursday January 11th 2024                                     #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Thu Jan 11 2024                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2024 OpenPlains Inc.                                           #
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


class MapsetResponseModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    bounding_box = serializers.CharField()  # bbox in WGS84 geojson format
    size = serializers.IntegerField()  # in bytes
    lock_status = serializers.BooleanField()
    num_raster_layers = serializers.IntegerField()
    num_vector_layers = serializers.IntegerField()
    description = serializers.CharField()
    created_date = serializers.DateTimeField()
    last_edited_date = serializers.DateTimeField()
