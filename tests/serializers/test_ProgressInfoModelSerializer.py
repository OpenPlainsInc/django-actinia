###############################################################################
# Filename: test_ProgressInfoModelSerializer.py                                #
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

from django.test import TestCase
from rest_framework import serializers
from grass.serializers.ProgressInfoModelSerializer import ProgressInfoModelSerializer


class ProgressInfoModelSerializerTest(TestCase):
    def test_serializer_fields(self):
        serializer = ProgressInfoModelSerializer()
        expected_fields = ["step", "num_of_steps", "sub_step", "num_of_sub_steps"]
        self.assertEqual(set(serializer.fields.keys()), set(expected_fields))

    def test_serializer_field_types(self):
        serializer = ProgressInfoModelSerializer()
        self.assertIsInstance(serializer.fields["step"], serializers.IntegerField)
        self.assertIsInstance(
            serializer.fields["num_of_steps"], serializers.IntegerField
        )
        self.assertIsInstance(serializer.fields["sub_step"], serializers.IntegerField)
        self.assertIsInstance(
            serializer.fields["num_of_sub_steps"], serializers.IntegerField
        )
