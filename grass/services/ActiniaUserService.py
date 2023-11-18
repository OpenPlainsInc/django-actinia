###############################################################################
# Filename: ActiniaUserService.py                                              #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday November 13th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Nov 17 2023                                               #
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

"""
This module contains the ActiniaUserService class and related functions for managing Actinia users and projects.

The ActiniaUserService class provides methods for interacting with the Actinia REST API for GRASS GIS, including creating and deleting users, retrieving user information, and managing user projects (locations) and mapsets.

The module also includes helper functions for populating mapsets and locations, as well as logging and error handling.

Note: This module requires the actinia_openapi_python_client library and the Django framework.
"""

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
from grass.serializers import UserInfoResponseSerializer
from grass.serializers.UserListResponseSerializer import UserListResponseSerializer
from grass.serializers.ActiniaSimpleResponseSerializer import ResponseStatusSerializer


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


class ActiniaUserService:

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
                self.api_instance = actinia_openapi_python_client.UserManagementApi(
                    api_client
                )
        except Exception as e:
            self.logger.error(
                f"Exception occurred during Actinia user service initialization: {e}"
            )
            raise

    def get_actinia_users(self):
        """
        List all Actinia Users
        """
        try:
            api_response = self.api_instance.users_get()
            serializer = UserListResponseSerializer(data=api_response.to_dict())
            if serializer.is_valid():
                # Check if users exist in database
                return JsonResponse(serializer.data, status=200)
        except ApiException as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get_actinia_user(self, user_id):
        """
        Returns the actinia user for the user_id
        """
        try:
            api_response = self.api_instance.users_user_id_get(user_id)
            serializer = UserInfoResponseSerializer(data=api_response.to_dict())
            return JsonResponse(serializer.data)
        except ApiException as e:
            self.logger.error(
                f"Exception when calling UserManagementApi->users_user_id_get: {e}"
            )
            return JsonResponse({"error": str(e)}, status=400)

    @transaction.atomic
    def create_actinia_user(self, user, user_id, password, group=RolesEnum.USER.value):
        """
        Creates the actinia user for the user_id
        """
        from grass.models.ActiniaUser import ActiniaUser

        print("user_id: ", user_id)
        print("password: ", password)
        print("group: ", group)
        try:
            api_response = self.api_instance.users_user_id_post(
                user_id=user_id, password=password, group=group
            )
            print("api_response: ", api_response)
            # serializer = ResponseStatusSerializer(data=api_response)

            # if serializer.is_valid():

            actinia_user = ActiniaUser.objects.create(
                actinia_username=user_id,
                password=password,
                actinia_role=group,
                user=user,
            )
            self.logger.info(
                f"ActiniaUser created when calling UserManagementApi->users_user_id_post: {user_id}"
            )
            return actinia_user
        except ApiException as e:
            self.logger.error(
                f"Exception when calling UserManagementApi->users_user_id_post: {e}"
            )
            raise Exception(
                f"Exception when calling UserManagementApi->users_user_id_post: {e}"
            )

    @transaction.atomic
    def delete_actinia_user(self, actinia_user):
        """
        Deletes the actinia user for the user_id
        """
        try:
            actinia_user_id = actinia_user.actinia_username
            api_response = self.api_instance.users_user_id_delete(actinia_user_id)
            serializer = ResponseStatusSerializer(api_response)
            if api_response == 204:
                actinia_user.delete()
            return JsonResponse(serializer.data)
        except ApiException as e:
            self.logger.error(
                f"Exception when calling UserManagementApi->users_user_id_delete: {e}"
            )
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            self.logger.error(f"Exception occurred: {e}")
            return JsonResponse({"error": "An error occurred"}, status=500)

    def get_actinia_user_projects(self, user):
        """
        Returns a list of projects (Locations) for the user
        """
        pass

    def create_actinia_user_project(
        self, user, project_name, project_description, project_epsg
    ):
        """
        Creates a project (Location) for the user
        """
        pass

    # def delete_actinia_user_project(self, user, project_name):
    #     """
    #     Deletes a project (Location) for the user
    #     """
    #     pass

    # def get_actinia_user_project_mapsets(self, user, project_name):
    #     """
    #     Returns a list of mapsets for the project
    #     """
    #     pass

    # def create_actinia_user_project_mapset(self, user, project_name, mapset_name):
    #     """
    #     Creates a mapset for the project
    #     """
    #     pass

    # def create_actinia_user_token(self, user_id, expiration_time=None, api_key=False):
    #     """
    #     Generate authorization token for user and store in Tokens
    #     """
    #     base_url = self.__base_url
    #     Token.generate_actinia_token(
    #         base_url=base_url, actinia_user=self, api_key=True, expiration_time=None
    #     )

    # def get_user_modules(self):
    #     """
    #     Returns a list of modules available to the user
    #     """
    #     pass

    # def get_api_log(request, user_id):
    #     configuration = actinia_openapi_python_client.Configuration(
    #         host=ACTINIA_SETTINGS["ACTINIA_BASEURL"]
    #     )

    #     configuration = actinia_openapi_python_client.Configuration(
    #         username=ACTINIA_SETTINGS["ACTINIA_USER"],
    #         password=ACTINIA_SETTINGS["ACTINIA_PASSWORD"],
    #     )

    #     with actinia_openapi_python_client.ApiClient(configuration) as api_client:
    #         api_instance = actinia_openapi_python_client.APILogApi(api_client)

    #         try:
    #             api_response = api_instance.api_log_user_id_get(user_id)
    #             serializer = APILogSerializer(api_response)
    #             return JsonResponse(serializer.data)
    #         except ApiException as e:
    #             return JsonResponse({"error": str(e)}, status=400)
