###############################################################################
# Filename: test_ActiniaProjectService.py                                      #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday April 1st 2024                                          #
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
        project_name = "test_location_name"
        project_epsg = 2264
        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location(project_name, project_epsg)
        )
        response = self.project_service.create_project(project_name, project_epsg)
        self.assertIsInstance(response, dict)
        self.assertEqual(response["status"], "finished")
        self.assertEqual(
            response["message"], f"Location <{project_name}> successfully created"
        )

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    def test_create_project_already_exists(self, mock_locations_location_name_post):
        project_name = "test_location_name"
        project_epsg = 2264
        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location_error(project_name, project_epsg)
        )
        response = self.project_service.create_project(project_name, project_epsg)
        self.assertIsInstance(response, dict)
        self.assertEqual(response["status"], "error")
        self.assertEqual(
            response["message"],
            f"Unable to create location. Location <{project_name}> exists in user database.",
        )

    @patch("actinia_openapi_python_client.LocationManagementApi.locations_get")
    def test_get_projects(self, mock_locations_get):
        location_list = ["test_locations"]
        mock_locations_get.return_value = ActiniaLocationsAPIMocks.get_locations(
            location_list
        )
        response = self.project_service.get_projects()
        expected_response = {"locations": location_list, "status": "success"}
        self.assertIsInstance(response, dict)
        self.assertEqual(response, expected_response)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_info_get"
    )
    def test_get_project(self, mock_locations_location_name_info_get):
        location_name = "test_location_name"
        mock_locations_location_name_info_get.return_value = (
            ActiniaLocationsAPIMocks.get_location_info(location_name)
        )
        response = self.project_service.get_project(location_name)
        self.assertIsInstance(response, dict)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_info_get"
    )
    def test_get_project_error(self, mock_locations_location_name_info_get):
        location_name = "fake_test_location_name"
        mock_locations_location_name_info_get.return_value = (
            ActiniaLocationsAPIMocks.get_location_info_error(location_name)
        )
        response = self.project_service.get_project(location_name)
        self.assertIsInstance(response, dict)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_delete"
    )
    def test_delete_project(self, mock_locations_location_name_delete):
        location_name = "test_location_name"
        mock_locations_location_name_delete.return_value = (
            ActiniaLocationsAPIMocks.delete_location(location_name)
        )
        expected_response = {
            "message": f"location {location_name} deleted",
            "status": "success",
        }
        response = self.project_service.delete_project(location_name)
        self.assertIsInstance(response, dict)
        self.assertEqual(response, expected_response)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_delete"
    )
    def test_delete_project_error(self, mock_locations_location_name_delete):
        location_name = "fake_test_location_name"
        mock_locations_location_name_delete.return_value = (
            ActiniaLocationsAPIMocks.delete_location_error(location_name)
        )
        expected_response = {
            "message": f"location {location_name} does not exists",
            "status": "error",
        }
        response = self.project_service.delete_project(location_name)
        self.assertIsInstance(response, dict)
        self.assertEqual(response, expected_response)
