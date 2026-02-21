###############################################################################
# Filename: test_LocationDetailSerializer.py                                   #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday February 2025                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
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

from django.test import TestCase
from grass.serializers.LocationDetailSerializer import (
    extract_bbox_from_wkt,
    extract_unit_from_wkt,
)

# Sample WKT strings used in tests
PROJECTED_WKT = (
    'PROJCRS["NAD83(HARN) / North Carolina",'
    'BASEGEOGCRS["NAD83(HARN)",DATUM["NAD83 (High Accuracy Reference Network)",'
    'ELLIPSOID["GRS 1980",6378137,298.257222101,LENGTHUNIT["metre",1]]],'
    'PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],'
    'ID["EPSG",4152]],'
    'CONVERSION["SPCS83 North Carolina zone (meters)",'
    'METHOD["Lambert Conic Conformal (2SP)",ID["EPSG",9802]]],'
    'CS[Cartesian,2],AXIS["easting (X)",east,ORDER[1],LENGTHUNIT["metre",1]],'
    'AXIS["northing (Y)",north,ORDER[2],LENGTHUNIT["metre",1]],'
    'USAGE[SCOPE["Engineering survey."],AREA["United States."],'
    'BBOX[33.83,-84.33,36.59,-75.38]],ID["EPSG",3358]]'
)

GEOGRAPHIC_WKT = (
    'GEOGCRS["WGS 84",DATUM["World Geodetic System 1984",'
    'ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]]],'
    'PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],'
    'CS[ellipsoidal,2],AXIS["latitude",north,ORDER[1],'
    'ANGLEUNIT["degree",0.0174532925199433]],'
    'AXIS["longitude",east,ORDER[2],'
    'ANGLEUNIT["degree",0.0174532925199433]],'
    'USAGE[SCOPE["Horizontal component of 3D system."],AREA["World."],'
    'BBOX[-90,-180,90,180]],ID["EPSG",4326]]'
)


class ExtractBboxFromWktTests(TestCase):
    def test_projected_crs_bbox(self):
        result = extract_bbox_from_wkt(PROJECTED_WKT)
        self.assertEqual(result, [33.83, -84.33, 36.59, -75.38])

    def test_geographic_crs_bbox(self):
        result = extract_bbox_from_wkt(GEOGRAPHIC_WKT)
        self.assertEqual(result, [-90.0, -180.0, 90.0, 180.0])

    def test_no_bbox(self):
        result = extract_bbox_from_wkt('PROJCRS["Test",CS[Cartesian,2]]')
        self.assertIsNone(result)

    def test_empty_string(self):
        result = extract_bbox_from_wkt("")
        self.assertIsNone(result)

    def test_none_input(self):
        result = extract_bbox_from_wkt(None)
        self.assertIsNone(result)


class ExtractUnitFromWktTests(TestCase):
    def test_projected_crs_unit_metres(self):
        result = extract_unit_from_wkt(PROJECTED_WKT)
        self.assertEqual(result, "meters")

    def test_geographic_crs_unit_degrees(self):
        # Geographic CRS: no LENGTHUNIT at top-level axes, only ANGLEUNIT
        geographic_no_lengthunit = (
            'GEOGCRS["WGS 84",DATUM["World Geodetic System 1984"],'
            "CS[ellipsoidal,2],"
            'AXIS["latitude",north,ORDER[1],ANGLEUNIT["degree",0.0174532925199433]],'
            "BBOX[-90,-180,90,180]]"
        )
        result = extract_unit_from_wkt(geographic_no_lengthunit)
        self.assertEqual(result, "degrees")

    def test_foot_unit(self):
        wkt_with_foot = (
            'PROJCRS["Test",CS[Cartesian,2],'
            'AXIS["easting",east,LENGTHUNIT["foot",0.3048]],'
            "BBOX[0,0,1,1]]"
        )
        result = extract_unit_from_wkt(wkt_with_foot)
        self.assertEqual(result, "feet")

    def test_no_unit(self):
        result = extract_unit_from_wkt('PROJCRS["Test",CS[Cartesian,2]]')
        self.assertIsNone(result)

    def test_empty_string(self):
        result = extract_unit_from_wkt("")
        self.assertIsNone(result)

    def test_none_input(self):
        result = extract_unit_from_wkt(None)
        self.assertIsNone(result)
