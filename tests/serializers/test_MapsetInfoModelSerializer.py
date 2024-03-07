###############################################################################
# Filename: test_MapsetInfoModelSerializer.py                                  #
# Project: OpenPlains Inc.                                                     #
# File Created: Sunday December 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Wed Mar 06 2024                                               #
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

from django.test import TestCase
from grass.serializers import MapsetInfoModelSerializer


class MapsetInfoModelSerializerTestCase(TestCase):
    def test_serialization(self):
        data = {
            "projection": "EPSG:4326",
            "region": {
                "w": 0.0,
                "s": 0.0,
                "e": 10.0,
                "n": 10.0,
            },
        }
        serialized_data = MapsetInfoModelSerializer(data=data)
        self.assertTrue(serialized_data.is_valid())
        # self.assertEqual(serialized_data.data, data)

    def test_deserialization(self):
        data = {
            "projection": "EPSG:4326",
            "region": {
                "w": 0.0,
                "s": 0.0,
                "e": 10.0,
                "n": 10.0,
            },
        }
        deserialized_data = MapsetInfoModelSerializer(data=data)
        self.assertTrue(deserialized_data.is_valid())
