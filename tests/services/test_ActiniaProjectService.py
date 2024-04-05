###############################################################################
# Filename: test_ActiniaProjectService.py                                      #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday April 1st 2024                                          #
# Author: Srihitha Reddy Kaalam (srihithareddykaalam@gmail.com)                #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Monday April 1st 2024                                         #
# Modified By: Srihitha Reddy Kaalam                                           #
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
from grass.models import Location
from grass.services.ProjectService import ProjectService
from django.contrib.auth.models import User
from ..mocks.ActiniaLocationsMocks import ActiniaLocationsAPIMocks
from unittest.mock import patch


class TestActiniaProjectService(TestCase):
    def setUp(self):
        self.project_service = ProjectService()

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    def test_create_project(self, mock_locations_location_name_post):
        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location("test_location_name", 2264)
        )
        project_name = "test_location_name"
        project_epsg = 2264
        response = self.project_service.create_project(project_name, project_epsg)
        self.assertIsInstance(response, JsonResponse)
        response_data = response.json()
        self.assertEqual(response_data["status"], "finished")
        self.assertEqual(
            response_data["message"], f"Location <{project_name}> successfully created"
        )

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    def test_create_project_already_exists(self, mock_locations_location_name_post):
        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location_error("test_location_name", 2264)
        )
        with self.assertRaises(Exception):
            project_name = "test_location_name"
            project_epsg = 2264
            self.project_service.create_project(project_name, project_epsg)

    @patch("actinia_openapi_python_client.LocationManagementApi.locations_get")
    def test_get_projects(self, mock_locations_get):
        mock_locations_get.return_value = ActiniaLocationsAPIMocks.get_locations(
            ["test_locations"]
        )
        response = self.project_service.get_projects()
        self.assertIsInstance(response, JsonResponse)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_info_get"
    )
    def test_get_project(self, mock_locations_location_name_info_get):
        location_name = "test_location_name"
        mock_locations_location_name_info_get.return_value = (
            ActiniaLocationsAPIMocks.get_location_info(location_name)
        )
        response = self.project_service.get_project(location_name)
        self.assertIsInstance(response, JsonResponse)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_info_get"
    )
    def test_get_project_error(self, mock_locations_location_name_info_get):
        location_name = "fake_test_location_name"
        mock_locations_location_name_info_get.return_value = (
            ActiniaLocationsAPIMocks.get_location_info_error(location_name)
        )
        response = self.project_service.get_project(location_name)
        self.assertIsInstance(response, JsonResponse)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_delete"
    )
    def test_delete_project(self, mock_locations_location_name_delete):
        location_name = "test_location_name"
        mock_locations_location_name_delete.return_value = (
            ActiniaLocationsAPIMocks.delete_location(location_name)
        )
        response = self.project_service.delete_project(location_name)
        self.assertIsInstance(response, JsonResponse)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_delete"
    )
    def test_delete_project_error(self, mock_locations_location_name_delete):
        location_name = "fake_test_location_name"
        mock_locations_location_name_delete.return_value = (
            ActiniaLocationsAPIMocks.delete_location_error(location_name)
        )
        response = self.project_service.delete_project(location_name)
        self.assertIsInstance(response, JsonResponse)
