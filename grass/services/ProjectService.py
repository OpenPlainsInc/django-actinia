###############################################################################
# Filename: ProjectService.py                                                  #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday November 21st 2023                                     #
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

import os
import requests
from enum import Enum, unique
from django.utils.crypto import get_random_string
from actinia import Actinia
from django.conf import settings
from grass.models.enums import RolesEnum
from requests.auth import HTTPBasicAuth
import logging
from grass.models import Token

import actinia_openapi_python_client
from actinia_openapi_python_client.rest import ApiException
from rest_framework import serializers
from django.http import JsonResponse
from grass.models import Location, Mapset
from grass.serializers.LocationResponseSerializer import LocationResponseSerializer
from grass.serializers.UserListResponseSerializer import UserListResponseSerializer
from grass.serializers.ProcessingResponseSerializer import ProcessingResponseSerializer
from grass.serializers.MapsetInfoResponseSerializer import MapsetInfoResponseSerializer
from grass.serializers.ResponseStatusSerializer import ResponseStatusSerializer


from django.db import transaction

ACTINIA_SETTINGS = settings.ACTINIA


def populate_mapsets(actinia_user, location_model, mapsets):
    """
    Populates Mapset objects from the mapsets list.

    Args:
        user (User): The user.
        location_models (list): A list of locations.
        mapsets (list): A list of mapsets.

    Returns:
        ActiniaUser: The actinia user.
    """
    if not isinstance(location_model, Location):
        raise Exception("Invalid location type")

    if not mapsets or not isinstance(mapsets, list):
        raise Exception("No mapsets provided or invalid mapset type")

    mapset_models = [
        Mapset(
            name=mapset,
            description="",
            owner=actinia_user.owner,
            location=location_model,
        )
        for mapset in mapsets
    ]

    Mapset.objects.bulk_create(mapset_models)
    return actinia_user


def populate_locations_mapsets(user, actinia_user, epsg, **kwargs):
    """
    Populates Location objects from the locations list.

    Args:
        user (User): The user.
        actinia_user (ActiniaUser): The actinia user.
        epsg (int): The EPSG code for the location.
        locations (list): A list of locations.
        mapsets (list): A list of mapsets.

    Returns:
        ActiniaUser: The actinia user.
    """
    locations = kwargs.get("locations")
    mapsets = kwargs.get("mapsets")

    if not locations or not isinstance(locations, list):
        raise Exception("No locations provided or invalid location type")

    location_models = [
        Location(owner=user, name=location["name"], epsg=location["epsg"])
        for location in locations
    ]

    Location.objects.bulk_create(location_models)

    if mapsets and isinstance(mapsets, list):
        for location_model in location_models:
            populate_mapsets(actinia_user, location_model, mapsets)

    return actinia_user


class ProjectService:
    """Manage GRASS GIS projects (Locations and Mapsets) for users"""

    # locations_get 	GET /locations 	Get a list of all available locations
    # locations_location_name_delete 	DELETE /locations/{location_name} 	Delete an existing location and everything inside from the user
    # locations_location_name_info_get 	GET /locations/{location_name}/info 	Get the location projection and current computational region of the
    # locations_location_name_post 	POST /locations/{location_name} 	Create a new location based on EPSG code in the user database.

    logger = logging.getLogger(__name__)

    def __init__(self):
        try:
            print("ACTINIA_BASEURL: ", ACTINIA_SETTINGS["ACTINIA_BASEURL"])
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
            serializer = LocationResponseSerializer(data=api_response.to_dict())
            if serializer.is_valid():
                return JsonResponse(serializer.data, status=200)
        except ApiException as e:
            return JsonResponse({"error": str(e)}, status=400)

    @transaction.atomic
    def create_project(self, user, project_name, project_description, project_epsg):
        """
        Create a project (Location) for the user
        """
        try:
            api_response = self.api_instance.locations_location_name_post(
                location_name=project_name, epsg=project_epsg
            )
            serializer = ProcessingResponseSerializer(data=api_response.to_dict())
            if serializer.is_valid():
                Location.objects.create(
                    owner=user,
                    name=project_name,
                    description=project_description,
                    epsg=project_epsg,
                )
                return JsonResponse(serializer.data, status=201)
        except ApiException as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get_project(self, project_name):
        """
        Get a project (Location) for the user
        """
        try:
            api_response = self.api_instance.locations_location_name_info_get(
                location_name=project_name
            )
            serializer = MapsetInfoResponseSerializer(data=api_response.to_dict())
            if serializer.is_valid():
                return JsonResponse(serializer.data, status=200)
        except ApiException as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete_project(self, project_name):
        """
        Delete a project (Location) for the user
        """
        try:
            api_response = self.api_instance.locations_location_name_delete(
                location_name=project_name
            )
            serializer = ResponseStatusSerializer(data=api_response.to_dict())
            if serializer.is_valid():
                return JsonResponse(serializer.data, status=200)
        except ApiException as e:
            return JsonResponse({"error": str(e)}, status=400)
