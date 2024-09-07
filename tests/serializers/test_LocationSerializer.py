###############################################################################
# Filename: test_LocationSerializer.py                                         #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday September 3rd 2024                                     #
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


from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from grass.models import Location, ActiniaUser
from grass.serializers import LocationSerializer
from ..mocks.ActiniaLocationsMocks import ActiniaLocationsAPIMocks
from ..mocks.ActiniaUsersAPIMocks import ActiniaUsersAPIMocks
from grass.models.enums import RolesEnum
from unittest.mock import patch, AsyncMock
from django.test import TransactionTestCase

User = get_user_model()


class LocationSerializerTest(TransactionTestCase):
    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_post")
    def setUp(self, mock_users_user_id_post, mock_locations_location_name_post):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.factory = RequestFactory()
        self.request = self.factory.post("/location/", format="json")
        self.request.user = self.user
        mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user(
            self.user.username
        )

        self.actinia_user = self.user.actinia_user
        self.location_data = {
            "name": "Test_Location",
            "epsg": "4326",
            "public": True,
            "slug": "test-location",
            "description": "A test location",
            "owner": self.user.id,
            "actinia_users": [],
        }

        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location(
                self.location_data["name"], self.location_data["epsg"]
            )
        )

        self.location = Location.objects.create(
            name=self.location_data["name"],
            epsg=self.location_data["epsg"],
            public=self.location_data["public"],
            slug=self.location_data["slug"],
            description=self.location_data["description"],
            owner=self.user,
        )
        self.location.actinia_users.set([self.actinia_user])
        self.serializer = LocationSerializer(instance=self.location)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "name",
                "epsg",
                "public",
                "slug",
                "description",
                "actinia_users",
                "owner",
                "created_on",
                "created_by",
                "updated_on",
                "updated_by",
            ],
        )

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.location_data["name"])

    def test_epsg_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["epsg"], self.location_data["epsg"])

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    def test_deserialization(self, mock_locations_location_name_post):
        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location(
                self.location_data["name"], self.location_data["epsg"]
            )
        )
        self.location_data["name"] = "Test_Location_2"
        serializer = LocationSerializer(
            data=self.location_data, context={"request": self.request}
        )

        self.assertTrue(serializer.is_valid())
        location = serializer.save()
        self.assertEqual(location.name, self.location_data["name"])

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    def test_invalid_location_name(self, mock_locations_location_name_post):
        """Location names shouldnt have spaces"""
        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location(
                "Test Location", self.location_data["epsg"]
            )
        )
        self.location_data["name"] = "Test Location"
        serializer = LocationSerializer(
            data=self.location_data, context={"request": self.request}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
