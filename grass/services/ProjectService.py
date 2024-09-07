###############################################################################
# Filename: ProjectService.py                                                  #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday November 21st 2023                                     #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Sep 06 2024                                               #
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

import os
import requests
from enum import Enum, unique
from django.utils.crypto import get_random_string
from django.conf import settings
from grass.models.enums import RolesEnum
from requests.auth import HTTPBasicAuth
import logging

# from grass.models import Token

import actinia_openapi_python_client
from actinia_openapi_python_client.rest import ApiException

# from rest_framework import serializers
from django.http import JsonResponse
from grass.serializers import LocationResponseSerializer

# from grass.serializers.UserListResponseSerializer import UserListResponseSerializer
from grass.serializers import ProcessingResponseSerializer
from grass.serializers import MapsetInfoResponseSerializer
from grass.serializers import ResourceStatusSerializer, ResponseStatusSerializer
from grass.models.enums import ResponseStatusEnum, ResourceStatusEnum

from actinia_openapi_python_client.models.projection_info_model import (
    ProjectionInfoModel,
)

ACTINIA_SETTINGS = settings.ACTINIA


class ProjectService:
    """Manage GRASS GIS projects (Locations and Mapsets) for users"""

    # locations_get 	GET /locations 	Get a list of all available locations
    # locations_location_name_delete 	DELETE /locations/{location_name} 	Delete an existing location and everything inside from the user
    # locations_location_name_info_get 	GET /locations/{location_name}/info 	Get the location projection and current computational region of the
    # locations_location_name_post 	POST /locations/{location_name} 	Create a new location based on EPSG code in the user database.

    logger = logging.getLogger(__name__)

    def __init__(self):
        try:
            configuration = actinia_openapi_python_client.Configuration(
                host=f'{ACTINIA_SETTINGS["ACTINIA_BASEURL"]}/api/v3/',
                username=ACTINIA_SETTINGS["ACTINIA_USER"],
                password=ACTINIA_SETTINGS["ACTINIA_PASSWORD"],
            )
            with actinia_openapi_python_client.ApiClient(configuration) as api_client:
                self.api_instance = actinia_openapi_python_client.LocationManagementApi(
                    api_client
                )
        except Exception as e:
            self.logger.error(
                f"Exception occurred during Actinia Location service initialization: {e}"
            )
            raise

    def get_projects(self):
        """
        List all projects (Locations) for the user
        """
        try:
            api_response = self.api_instance.locations_get()
            serializer = LocationResponseSerializer(data=api_response)
            if serializer.is_valid():
                if serializer.data["status"] == ResponseStatusEnum.SUCCESS.label:
                    # Check if locations exist in database
                    return serializer.data
                else:
                    self.logger.warning(
                        f"ActiniaLocations retrevial warning: {serializer.data}"
                    )
                    return serializer.data
            else:
                self.logger.error(
                    f"LocationResponseSerializer Serialization Error: {serializer.errors}"
                )
                return serializer.errors
        except ApiException as e:
            self.logger.error(
                f"Exception when calling LocationManagementApi->locations_get: {e}"
            )

    def create_project(self, project_name, project_epsg):
        """
        Create a project (Location) for the user
        """
        try:
            epsg = ProjectionInfoModel(epsg=str(project_epsg))
            api_response = self.api_instance.locations_location_name_post(
                location_name=project_name, epsg_code=epsg
            )

            self.logger.info(f"create_project.api_response: {api_response}")
            serializer = ProcessingResponseSerializer(data=api_response)
            if serializer.is_valid():
                self.logger.info(
                    f"Create Project Serialized Response: {serializer.data}"
                )
                if serializer.data["status"] == ResourceStatusEnum.FINISHED.label:
                    self.logger.info(f"Location created: {project_name}")
                    return serializer.data
                else:
                    self.logger.error(f"Error: {serializer.data}")
                    return serializer.data
            else:
                self.logger.error(
                    f"ProcessingResponseSerializer Serialization Error: {serializer.errors}"
                )
                return serializer.errors
        except ApiException as e:
            self.logger.error(
                f"Exception when calling LocationManagementApi->locations_location_name_post: {e}"
            )

    def get_project(self, project_name):
        """
        Get a project (Location) for the user
        """
        try:
            api_response = self.api_instance.locations_location_name_info_get(
                project_name
            )
            serializer = MapsetInfoResponseSerializer(data=api_response)
            if serializer.is_valid():
                if serializer.data["status"] == "finished":
                    self.logger.info(f"ActiniaLocation retrieved: {project_name}")
                    return serializer.data
                else:
                    self.logger.error(
                        f"ActiniaLocation retrieval failed: {serializer.data['message']}"
                    )
                    return serializer.data
            else:
                self.logger.error(
                    f"MapsetInfoResponseSerializer Serialization Error: {serializer.errors}"
                )
                return serializer.errors

        except ApiException as e:
            self.logger.error(
                f"Exception when calling LocationManagementApi->locations_location_name_info_get: {e}"
            )

    def delete_project(self, project_name):
        """
        Delete a project (Location) for the user
        """
        try:
            location_name = project_name
            api_response = self.api_instance.locations_location_name_delete(
                location_name
            )
            serializer = ResponseStatusSerializer(data=api_response)
            if serializer.is_valid():
                if serializer.data["status"] == ResponseStatusEnum.SUCCESS.label:
                    self.logger.info(f"ActiniaProject deleted: {location_name}")
                    return serializer.data
                else:
                    self.logger.error(
                        f"ActiniaProject deletion failed: {serializer.data['message']}"
                    )
                    return serializer.data
            else:
                self.logger.error(
                    f"ResponseStatusSerializer Serialization Error: {serializer.errors}"
                )
                return serializer.errors
        except ApiException as e:
            self.logger.error(
                f"Exception when calling LocationManagementApi->locations_location_name_delete: {e}"
            )
