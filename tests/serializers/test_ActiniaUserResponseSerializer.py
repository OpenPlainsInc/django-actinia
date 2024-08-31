###############################################################################
# Filename: test_ActiniaUserResponseSerializer.py                              #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday November 17th 2023                                      #
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

from django.contrib.auth.models import User
from django.test import TestCase
from grass.serializers import (
    ActiniaUserResponseSerializer,
)
from grass.models.enums import RolesEnum
from grass.models.ActiniaUser import ActiniaUser
from unittest.mock import patch
from ..mocks.ActiniaUsersAPIMocks import ActiniaUsersAPIMocks


class ActiniaUserResponseSerializerTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        with patch(
            "actinia_openapi_python_client.UserManagementApi.users_user_id_delete"
        ) as mock_users_user_id_delete:
            mock_users_user_id_delete.return_value = ActiniaUsersAPIMocks.delete_user(
                cls.defaultVars["username"]
            )
            # Clean up any resources that were created in the setUpTestData() classmethod or by the test methods
            cls.actinia_user.delete()
            cls.user.delete()

    @classmethod
    def setUpTestData(cls):

        with patch(
            "actinia_openapi_python_client.UserManagementApi.users_user_id_post"
        ) as mock_users_user_id_post:

            cls.defaultVars = {
                "username": "actiniatestuser3",
                "actinia_username": "actiniatestuser3",
                "email": "testuser@example.com",
                "password": "testpass",
                "actinia_role": RolesEnum.ADMIN.value,
            }

            mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user(
                cls.defaultVars["username"]
            )

            # Set up non-modified objects used by all test methods
            cls.user = User.objects.create(
                username=cls.defaultVars["username"],
                email=cls.defaultVars["email"],
                password=cls.defaultVars["password"],
            )

            cls.actinia_user = ActiniaUser.objects.create(
                user=cls.user,
                actinia_role=RolesEnum.ADMIN.value,
                actinia_username=cls.user.username,
                password="testpass",
            )
            cls.serializer_data = {
                "id": cls.actinia_user.id,
                "user_id": cls.actinia_user.user_id,
                "actinia_username": cls.user.username,
                "locations": [],
                "actinia_role": RolesEnum.ADMIN.value,
                "created_on": "2023-11-17T00:00:00Z",
                "updated_on": "2023-11-17T00:00:00Z",
                "created_by": "actiniatestuser3",
                "updated_by": "actiniatestuser3",
                # "modules": {}
            }
            cls.serializer = ActiniaUserResponseSerializer(instance=cls.actinia_user)

    def test_serializer_fields(self):
        self.assertIsInstance(self.actinia_user, ActiniaUser)
        self.assertEqual(
            self.actinia_user.actinia_username, self.defaultVars["actinia_username"]
        )
        self.assertEqual(
            self.actinia_user.actinia_role, self.defaultVars["actinia_role"]
        )
        self.assertEqual(self.actinia_user.user_id, self.user.id)

    def test_serializer_valid(self):
        serializer = ActiniaUserResponseSerializer(data=self.serializer_data)
        if serializer.is_valid():
            self.assertTrue(serializer.is_valid())
        else:
            print(serializer.errors)
            self.assertTrue(serializer.is_valid())
