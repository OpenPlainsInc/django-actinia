###############################################################################
# Filename: test_ProcessLogModelSerializer.py                                  #
# Project: OpenPlains Inc.                                                     #
# File Created: Sunday December 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Aug 30 2024                                               #
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
from rest_framework import serializers
from grass.serializers.ProcessLogModelSerializer import ProcessLogModelSerializer


class ProcessLogModelSerializerTest(TestCase):
    def setUp(self):
        self.serializer = ProcessLogModelSerializer()

    def test_serializer_fields(self):
        expected_fields = [
            "id",
            "executable",
            "parameter",
            "stdout",
            "stderr",
            "return_code",
            "run_time",
            "mapset_size",
        ]
        self.assertEqual(set(self.serializer.fields.keys()), set(expected_fields))

    def test_serializer_field_types(self):
        field_types = {
            "id": serializers.CharField,
            "executable": serializers.CharField,
            "parameter": serializers.ListField,
            "stdout": serializers.CharField,
            "stderr": serializers.ListField,
            "return_code": serializers.FloatField,
            "run_time": serializers.FloatField,
            "mapset_size": serializers.FloatField,
        }
        for field_name, field_type in field_types.items():
            self.assertIsInstance(self.serializer.fields[field_name], field_type)

    def test_serializer_required_fields(self):
        required_fields = ["executable", "parameter", "stdout", "return_code"]
        for field_name in required_fields:
            self.assertTrue(self.serializer.fields[field_name].required)

    def test_serializer_optional_fields(self):
        optional_fields = ["id", "run_time", "mapset_size"]
        for field_name in optional_fields:
            self.assertFalse(self.serializer.fields[field_name].required)
