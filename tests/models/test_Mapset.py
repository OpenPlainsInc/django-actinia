###############################################################################
# Filename: test_Mapset.py                                                     #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday October 20th 2023                                       #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Oct 20 2023                                               #
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
from actinia.models import Mapset, Location


class MapsetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        location = Location.objects.create(name="Test Location")
        Mapset.objects.create(name="Test Mapset", location=location)

    def test_layers_count(self):
        mapset = Mapset.objects.get(id=1)
        self.assertEqual(mapset.layers_count(), 0)

    def test_layers(self):
        mapset = Mapset.objects.get(id=1)
        self.assertQuerysetEqual(mapset.layers(), [])
