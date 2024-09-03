###############################################################################
# Filename: test_ActiniaUserResponseSerializer.py                              #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday November 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Sep 02 2024                                               #
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
from django.db import transaction
from rest_framework.exceptions import ValidationError
from grass.serializers.fields import ActiniaRoleChoiceField
from grass.services import ActiniaUserService


class ActiniaUserResponseSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )

        self.user_data = {
            "id": 1,
            "user_id": 1,
            "actinia_username": "testuser",
            "actinia_role": RolesEnum.ADMIN.label,
            "locations": [],
            "created_on": "2023-11-17T00:00:00Z",
            "updated_on": "2023-11-17T00:00:00Z",
            "created_by": self.user.get_username(),
            "updated_by": self.user.get_username(),
            "user_details": {},
        }

        self.actinia_user = ActiniaUser(
            id=1,
            user_id=1,
            actinia_username="testuser",
            actinia_role=RolesEnum.ADMIN.value,
            created_on="2023-11-17T00:00:00Z",
            updated_on="2023-11-17T00:00:00Z",
            created_by=self.user,
            updated_by=self.user,
        )

    # Creating a user in the setUp method is causing a the database connection to be closed
    # and the test to fail. The user is created in the test method instead.
    # def tearDown(self):
    #     self.user.delete()

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_get")
    @patch.object(ActiniaUserService, "get_actinia_user")
    def test_serializer_valid(self, mock_users_user_id_get, mock_get_actinia_user):

        mock_users_user_id_get.return_value = ActiniaUsersAPIMocks.get_user(
            user_id=self.user.username, user_role="admin"
        )

        mock_get_actinia_user.return_value = ActiniaUsersAPIMocks.get_user(
            self.user.username,
            user_role=self.user_data.get("actinia_role"),
            as_dict=True,
        )
        serializer = ActiniaUserResponseSerializer(data=self.user_data)
        if serializer.is_valid():
            print(f"test_serializer_valid: data: {serializer.data}")
        else:
            print(f"test_serializer_valid: errors: {serializer.errors}")

        self.assertTrue(serializer.is_valid())

    # @patch.object(ActiniaUserService, 'get_actinia_user')
    # def test_serializer_fields(self, mock_get_actinia_user):
    #     mock_get_actinia_user.return_value = ActiniaUsersAPIMocks.get_user(
    #         self.user.username, as_dict=True
    #     )
    #     serializer = ActiniaUserResponseSerializer(instance=self.actinia_user)
    #     print(f"test_serializer_fields: {serializer.data}")
    #     data = serializer.data
    #     self.assertEqual(set(data.keys()), set(self.user_data.keys()))

    # def test_serializer_valid(self):
    #     serializer = ActiniaUserResponseSerializer(data=self.user_data)
    #     self.assertTrue(serializer.is_valid())

    # def test_serializer_invalid(self):
    #     invalid_data = self.user_data.copy()
    #     invalid_data["actinia_role"] = "invalid_role"
    #     serializer = ActiniaUserResponseSerializer(data=invalid_data)
    #     with self.assertRaises(ValidationError):
    #         serializer.is_valid(raise_exception=True)

    # @patch.object(ActiniaUserService, 'get_actinia_user')
    # def test_get_user_details(self, mock_get_actinia_user):
    #     mock_get_actinia_user.return_value = {"detail": "user details"}
    #     serializer = ActiniaUserResponseSerializer(instance=self.actinia_user)
    #     user_details = serializer.get_user_details(self.actinia_user)
    #     self.assertEqual(user_details, {"detail": "user details"})
    #     mock_get_actinia_user.assert_called_once_with("testuser")

    # @patch.object(ActiniaUserService, 'get_actinia_user')
    # def test_get_user_details_exception(self, mock_get_actinia_user):
    #     mock_get_actinia_user.side_effect = Exception("Error fetching user details")
    #     serializer = ActiniaUserResponseSerializer(instance=self.actinia_user)
    #     user_details = serializer.get_user_details(self.actinia_user)
    #     self.assertEqual(user_details, {"error": "Error fetching user details"})
    #     mock_get_actinia_user.assert_called_once_with("testuser")

    # @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_get")
    # def test_serializer_valid(self, mock_users_user_id_get):
    #     print("test_serializer_valid")
    #     mock_users_user_id_get.return_value = ActiniaUsersAPIMocks.get_user(
    #         self.defaultVars["username"]
    #     )
    #     serializer = ActiniaUserResponseSerializer(instance=self.actinia_user)
    #     self.assertIsInstance(serializer, ActiniaUserResponseSerializer)
    #     self.assertTrue(serializer.is_valid())

    # @classmethod
    # def tearDownClass(cls):
    #     with patch(
    #         "actinia_openapi_python_client.UserManagementApi.users_user_id_delete"
    #     ) as mock_users_user_id_delete:
    #         mock_users_user_id_delete.return_value = ActiniaUsersAPIMocks.delete_user(
    #             cls.defaultVars["username"]
    #         )
    #         # Clean up any resources that were created in the setUpTestData() classmethod or by the test methods
    #         cls.actinia_user.delete()

    #         cls.user.delete()
