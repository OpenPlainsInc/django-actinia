###############################################################################
# Filename: test_ActiniaRoleChoiceField.py                                     #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday September 2nd 2024                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Sep 02 2024                                               #
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


from django.test import TestCase
from rest_framework import serializers
from grass.models.enums.RolesEnum import RolesEnum
from grass.serializers.fields.ActiniaRoleChoiceField import ActiniaRoleChoiceField


class TestActiniaRoleChoiceField(TestCase):
    def setUp(self):
        self.field = ActiniaRoleChoiceField()

    def test_init(self):
        self.assertIsInstance(self.field, serializers.ChoiceField)
        self.assertEqual(self.field.choices, RolesEnum.to_dict())
        self.assertFalse(self.field.allow_blank)

    def test_to_representation(self):
        self.assertEqual(self.field.to_representation(""), "")
        self.assertEqual(self.field.to_representation(None), None)
        self.assertEqual(self.field.to_representation("SU"), "superadmin")
        self.assertEqual(self.field.to_representation("AD"), "admin")
        self.assertEqual(self.field.to_representation("US"), "user")
        self.assertEqual(self.field.to_representation("GU"), "guest")

    def test_to_internal_value(self):
        self.assertEqual(self.field.to_internal_value("superadmin"), "SU")
        self.assertEqual(self.field.to_internal_value("admin"), "AD")
        self.assertEqual(self.field.to_internal_value("user"), "US")
        self.assertEqual(self.field.to_internal_value("guest"), "GU")
        self.assertRaises(serializers.ValidationError, self.field.to_internal_value, "")
        self.assertRaises(
            serializers.ValidationError, self.field.to_internal_value, None
        )
        self.assertRaises(
            serializers.ValidationError, self.field.to_internal_value, "invalid_role"
        )
