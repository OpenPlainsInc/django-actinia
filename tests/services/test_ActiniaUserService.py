###############################################################################
# Filename: test_ActiniaUserService.py                                         #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday November 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Wed Apr 10 2024                                               #
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
from django.http import JsonResponse
from actinia_openapi_python_client import ApiException
from grass.models import ActiniaUser
from grass.services.ActiniaUserService import ActiniaUserService
from django.contrib.auth.models import User
from ..mocks.ActiniaUsersAPIMocks import ActiniaUsersAPIMocks
from unittest.mock import patch


class TestActiniaUserService(TestCase):
    def setUp(self):
        self.actinia_user_service = ActiniaUserService()

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_post")
    def test_create_actinia_user_already_exists(self, mock_users_user_id_post):
        mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user_error(
            "test_user_id"
        )
        with self.assertRaises(Exception):
            user = self.user
            user_id = "test_user_id"
            password = "test_password"
            group = "admin"
            self.actinia_user_service.create_actinia_user(
                user, user_id, password, group
            )

    @patch("actinia_openapi_python_client.UserManagementApi.users_get")
    def test_get_actinia_users(self, mock_users_get):
        user_list = ["test_user_id"]
        mock_users_get.return_value = ActiniaUsersAPIMocks.get_users(user_list)
        response = self.actinia_user_service.get_actinia_users()
        expected_response = {"status": "success", "user_list": user_list}
        self.assertIsInstance(response, dict)
        self.assertEqual(response, expected_response)

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_get")
    def test_get_actinia_user(self, mock_users_user_id_get):
        user_id = "test_user_id"
        mock_users_user_id_get.return_value = ActiniaUsersAPIMocks.get_user(user_id)
        response = self.actinia_user_service.get_actinia_user(user_id)
        # expected_response = {"message": f"User <{user_id}> does not exist", "status": "error"}  # TODO: Fix this
        self.assertIsInstance(response, dict)
        # self.assertEqual(response, expected_response)  # TODO: Fix this

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_get")
    def test_get_actinia_user_error(self, mock_users_user_id_get):
        user_id = "fake_test_user_id"
        mock_users_user_id_get.return_value = ActiniaUsersAPIMocks.get_user_error(
            user_id
        )
        response = self.actinia_user_service.get_actinia_user(user_id)
        expected_response = {
            "message": f"User <{user_id}> does not exist",
            "status": "error",
        }
        self.assertIsInstance(response, dict)
        self.assertEqual(response, expected_response)

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_delete")
    def test_delete_actinia_user(self, mock_users_user_id_delete):
        user_id = "test_user_id"
        mock_users_user_id_delete.return_value = ActiniaUsersAPIMocks.delete_user(
            user_id
        )
        expected_response = {"status": "success", "message": f"User {user_id} deleted"}
        response = self.actinia_user_service.delete_actinia_user(user_id)
        self.assertIsInstance(response, dict)
        self.assertEqual(response, expected_response)

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_delete")
    def test_delete_actinia_user_error(self, mock_users_user_id_delete):
        user_id = "fake_test_user_id"
        mock_users_user_id_delete.return_value = ActiniaUsersAPIMocks.delete_user_error(
            user_id
        )
        expected_response = {
            "status": "error",
            "message": f"Unable to delete user {user_id}. User does not exist.",
        }
        response = self.actinia_user_service.delete_actinia_user(user_id)
        self.assertIsInstance(response, dict)
        self.assertEqual(response, expected_response)
