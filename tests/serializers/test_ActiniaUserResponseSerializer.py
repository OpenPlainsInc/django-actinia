###############################################################################
# Filename: test_ActiniaUserResponseSerializer.py                              #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday November 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Nov 21 2023                                               #
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

from django.contrib.auth.models import User
from django.test import TestCase
from grass.models.ActiniaUser import ActiniaUser
from grass.serializers.ActiniaUserResponseSerializer import (
    ActiniaUserResponseSerializer,
)


class ActiniaUserResponseSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username="actiniatestuser",
            email="testuser@example.com",
            password="testpass",
        )

        cls.actinia_user = ActiniaUser.create_actinia_user(cls.user, "admin")
        cls.serializer_data = {
            "id": cls.actinia_user.id,
            "user_id": cls.actinia_user.user_id,
            "actinia_username": cls.user.username,
            "locations": [],
            "actinia_role": cls.actinia_user.actinia_role,
            # "modules": {}
        }
        cls.serializer = ActiniaUserResponseSerializer(instance=cls.actinia_user)

    def test_serializer_fields(self):
        self.assertEqual(
            set(self.serializer_data.keys()), set(self.serializer.data.keys())
        )

    def test_serializer_data(self):
        self.assertEqual(self.serializer_data, self.serializer.data)

    def test_serializer_valid(self):
        serializer = ActiniaUserResponseSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_save(self):
        serializer = ActiniaUserResponseSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        actinia_user = serializer.save()
        self.assertIsInstance(actinia_user, ActiniaUser)
        self.assertEqual(actinia_user.actinia_username, "actiniatestuser")
        self.assertEqual(actinia_user.actinia_role, "admin")
        self.assertEqual(actinia_user.user_id, 2)

    @classmethod
    def tearDownClass(cls):
        # Clean up any resources that were created in the setUpTestData() classmethod or by the test methods
        cls.actinia_user.delete()
