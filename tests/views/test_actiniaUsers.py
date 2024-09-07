###############################################################################
# Filename: test_actiniaUsers.py                                               #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday September 6th 2024                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Sep 06 2024                                               #
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

from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.test import TransactionTestCase
from unittest.mock import patch
from grass.models import Location
from ..mocks.ActiniaUsersAPIMocks import ActiniaUsersAPIMocks
from ..mocks.ActiniaLocationsMocks import ActiniaLocationsAPIMocks


class ActiniaUserViewSetAPITestCase(
    APITestCase, URLPatternsTestCase, TransactionTestCase
):
    urlpatterns = [
        path("api/v1/", include("grass.urls")),
    ]

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_get")
    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_post")
    def setUp(self, mock_users_user_id_post, mock_users_user_id_get):
        # Create a user to authenticate requests
        mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user(
            "testuser"
        )
        mock_users_user_id_get.return_value = ActiniaUsersAPIMocks.get_user(
            self.user.username, as_dict=False
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Log in the user to generate an auth token or session
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Define some data for the tests

        self.actinia_user_data = {
            "user_id": self.user.id,
            "actinia_username": self.user.username,
            "actinia_role": self.user.actinia_user.actinia_role,
            "created_on": "2024-09-07T01:37:55.990205Z",
            "updated_on": "2024-09-07T01:37:55.990237Z",
            "created_by": self.user.username,
            "updated_by": None,
            "user_details": {},
            "projects": ["test-location"],
        }

        self.location_data = {
            "id": 0,
            "owner": self.user,
            "name": "Test_Location",
            "epsg": "4326",
            "public": True,
            "description": "Test Description",
            "slug": "test-location",
            "actinia_users": [],
        }
        # URL for the API endpoint
        self.url = reverse(
            "grass:actinia-user-list"
        )  # Assuming your API uses DRF router URLs

    def test_list_actinia_users(self):
        """Test the GET request for listing actinia users"""

        response = self.client.get(self.url)

        # Ensure the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(
            response.data.get("results")[0].get("actinia_username"), "testuser"
        )
        # Check the returned data
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_actinia_users(self):
        """Test the GET request for listing actinia users"""

        response = self.client.get(self.url, self.user.actinia_user.id)

        # Ensure the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.data.get("actinia_username"), "testuser")
        self.assertEqual(response.data.get("projects"), [])
        self.assertEqual(response.data.get("user_details.status"), "success")
        # Check the returned data
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_actinia_user(self):
        """Test creating an actina user (POST request)"""
        # First, create a location
        response = self.client.post(self.url, self.user.id, format="json")

        # Check if the location was updated correctly
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_actinia_user(self):
        """Test updating an actina user (PUT request)"""
        # First, create a location
        response = self.client.put(self.url, self.location_data, format="json")

        # Check if the location was updated correctly
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    @patch("actinia_openapi_python_client.LocationManagementApi.locations_get")
    def test_actinia_user_with_location(
        self,
        mock_locations_location_name_post,
        mock_locations_get,
    ):
        """Test deleting a location (DELETE request)"""

        # Mock the get locations response
        mock_locations_get.return_value = ActiniaLocationsAPIMocks.get_locations(
            location_list=[]
        )

        # Mock the create location response
        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location(
                self.location_data["name"], self.location_data["epsg"]
            )
        )

        # Create a location
        location = Location.objects.create(**self.location_data)

        response = self.client.get(self.url, self.user.actinia_user.id)

        # Ensure the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.data.get("actinia_username"), "testuser")
        self.assertEqual(response.data.get("projects"), [location.slug])
