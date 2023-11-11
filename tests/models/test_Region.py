###############################################################################
# Filename: test_Region.py                                                     #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday November 10th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Nov 10 2023                                               #
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
from actinia.models import Region


class RegionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Region.objects.create(
            zone=1,
            projection=4326,
            n=50.0,
            s=40.0,
            e=-70.0,
            w=-80.0,
            t=100.0,
            b=0.0,
            nsres=0.1,
            ewres=0.1,
            nsres3=0.1,
            ewres3=0.1,
            tbres=0.1,
            rows=100.0,
            cols=100.0,
            rows3=100.0,
            cols3=100.0,
            depths=1.0,
            cells=10000.0,
            cells3=1000000.0,
        )

    def test_zone_label(self):
        region = Region.objects.get(id=1)
        field_label = region._meta.get_field("zone").verbose_name
        self.assertEqual(field_label, "zone")

    def test_projection_label(self):
        region = Region.objects.get(id=1)
        field_label = region._meta.get_field("projection").verbose_name
        self.assertEqual(field_label, "projection")

    def test_n_label(self):
        region = Region.objects.get(id=1)
        field_label = region._meta.get_field("n").verbose_name
        self.assertEqual(field_label, "n")

    # Add more tests for other fields as needed
