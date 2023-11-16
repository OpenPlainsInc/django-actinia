###############################################################################
# Filename: ActiniaUserService.py                                              #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday November 13th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Wed Nov 15 2023                                               #
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
from grass.serializers import APILogSerializer, UserListResponseSerializer
from actinia_openapi_python_client.models.user_list_response_model import (
    UserListResponseModel,
)

ACTINIA_SETTINGS = settings.ACTINIA


@unique
class USER_TASK(Enum):
    USERS = "users"
    TOKEN = "token"
    API_KEY = "api_key"
    API_LOG = "api_log"


def __populate_locations_mapsets(self, locations):
    """
    Populates Location objects from the locations list.

    Args:
        locations (list): A list of locations.
    """

    location_models = [
        Location(owner=self, name=location["name"], epsg=location["epsg"])
        for location in locations
    ]

    Location.objects.bulk_create(location_models)

    for loc, loc_model in zip(locations, location_models):
        mapsets = loc.mapsets
        mapset_models = [
            Mapset(
                name=mapset.name,
                description="",
                owner=self.owner,
                location=loc_model,
            )
            for mapset in mapsets
        ]

        Mapset.objects.bulk_create(mapset_models)


class ActiniaUserService:
    configuration = actinia_openapi_python_client.Configuration(
        host=ACTINIA_SETTINGS["ACTINIA_BASEURL"]
    )

    configuration = actinia_openapi_python_client.Configuration(
        username=ACTINIA_SETTINGS["ACTINIA_USER"],
        password=ACTINIA_SETTINGS["ACTINIA_PASSWORD"],
    )

    __actinia_super_auth = HTTPBasicAuth(
        ACTINIA_SETTINGS["ACTINIA_USER"], ACTINIA_SETTINGS["ACTINIA_PASSWORD"]
    )

    @property
    def __base_url(self):
        # TODO: Add this full url to setting and enforce https
        ACTINIA_URL = os.path.join(
            "http://",
            ACTINIA_SETTINGS["ACTINIA_BASEURL"],
            "api",
            ACTINIA_SETTINGS["ACTINIA_VERSION"],
        )
        return ACTINIA_URL

    def __actinia_user_request_url(self, task, user_id=None):
        """
        Provides the url to an Actinia mapset resource.

        Parameters
        ----------
        actinia_url : str
            The base url to actinia server
        user_id : str
            The GRASS location name
            route: /locations/{location_name}/mapsets

        Returns
        -------
        base_url : str
            Return the url scheme for the mapset request
        """
        if task not in [e.value for e in USER_TASK]:
            raise Exception(f"Invalid user task: {task}")

        base_url = f"{self.__base_url}/{task}"
        if user_id is not None:
            base_url = f"{base_url}/{user_id}"

        return base_url

    def create_actinia_user_account(self, user, group, username, password):
        query_params = {"group": group, "password": password}

        url = self.__actinia_user_request_url(USER_TASK.USERS.value, username)

        print(f"Actinia Super Admin Auth: {self.__actinia_super_auth.username}")
        print(f"Actinia User Create URL: {url}")
        print(f"Actinia User Create Params: {query_params}")
        try:
            response = requests.post(
                url,
                auth=self.__actinia_super_auth,
                params=query_params,
                headers={"content-type": "application/json; charset=utf-8"},
            )
            if response.status_code != 201:
                raise Exception(
                    f"Failed to make post request to {url}: {response.status_code}, response: {response.json()}"
                )
        except Exception as e:
            print(e)
            raise

        print(f"Actinia User {username} created in group: {query_params['group']}")
        return True

    def get_actinia_users(self):
        configuration = actinia_openapi_python_client.Configuration(
            host=ACTINIA_SETTINGS["ACTINIA_BASEURL"]
        )

        configuration = actinia_openapi_python_client.Configuration(
            username=ACTINIA_SETTINGS["ACTINIA_USER"],
            password=ACTINIA_SETTINGS["ACTINIA_PASSWORD"],
        )

        with actinia_openapi_python_client.ApiClient(configuration) as api_client:
            api_instance = actinia_openapi_python_client.UserManagementApi(api_client)
            try:
                api_response = api_instance.users_get()
                serializer = UserListResponseSerializer(api_response)
                return JsonResponse(serializer.data)
            except ApiException as e:
                return JsonResponse({"error": str(e)}, status=400)

    def get_actinia_user_account(self, username):
        """
        Returns the actinia user account for the user_id
        """
        url = self.__actinia_user_request_url(USER_TASK.USERS.value, username)
        response = requests.get(
            url,
            auth=self.__actinia_super_auth,
            headers={"content-type": "application/json; charset=utf-8"},
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to get user: {url}: {response.status_code}, response: {response.json()}"
            )
        return response.json()

    def delete_actinia_user_account(self, actinia_username):
        """
        Deletes the actinia user account for the user_id
        """
        url = self.__actinia_user_request_url(USER_TASK.USERS.value, actinia_username)

        try:
            response = requests.delete(
                url,
                auth=self.__actinia_super_auth,
                headers={"content-type": "application/json; charset=utf-8"},
            )
            if response.status_code != 200:
                raise Exception(
                    f"Failed to delete user: {url}: {response.status_code}, response: {response.json()}"
                )
        except Exception as e:
            print(e)
            raise
        print(f"{response.json()}")
        return response.json()

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

    def delete_actinia_user_project(self, user, project_name):
        """
        Deletes a project (Location) for the user
        """
        pass

    def get_actinia_user_project_mapsets(self, user, project_name):
        """
        Returns a list of mapsets for the project
        """
        pass

    def create_actinia_user_project_mapset(self, user, project_name, mapset_name):
        """
        Creates a mapset for the project
        """
        pass

    def create_actinia_user_token(self, user_id, expiration_time=None, api_key=False):
        """
        Generate authorization token for user and store in Tokens
        """
        base_url = self.__base_url
        Token.generate_actinia_token(
            base_url=base_url, actinia_user=self, api_key=True, expiration_time=None
        )

    def get_user_modules(self):
        """
        Returns a list of modules available to the user
        """
        pass

    def get_api_log(request, user_id):
        configuration = actinia_openapi_python_client.Configuration(
            host=ACTINIA_SETTINGS["ACTINIA_BASEURL"]
        )

        configuration = actinia_openapi_python_client.Configuration(
            username=ACTINIA_SETTINGS["ACTINIA_USER"],
            password=ACTINIA_SETTINGS["ACTINIA_PASSWORD"],
        )

        with actinia_openapi_python_client.ApiClient(configuration) as api_client:
            api_instance = actinia_openapi_python_client.APILogApi(api_client)

            try:
                api_response = api_instance.api_log_user_id_get(user_id)
                serializer = APILogSerializer(api_response)
                return JsonResponse(serializer.data)
            except ApiException as e:
                return JsonResponse({"error": str(e)}, status=400)


class ApiKeySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    api_key = serializers.CharField()


def get_api_key(request, user_id):
    configuration = actinia_openapi_python_client.Configuration(
        host=ACTINIA_SETTINGS["ACTINIA_BASEURL"]
    )

    configuration = actinia_openapi_python_client.Configuration(
        username=ACTINIA_SETTINGS["ACTINIA_USER"],
        password=ACTINIA_SETTINGS["ACTINIA_PASSWORD"],
    )

    with actinia_openapi_python_client.ApiClient(configuration) as api_client:
        api_instance = actinia_openapi_python_client.APIKeyApi(api_client)

        try:
            api_response = api_instance.api_key_user_id_get(user_id)
            serializer = ApiKeySerializer(api_response)
            return JsonResponse(serializer.data)
        except ApiException as e:
            return JsonResponse({"error": str(e)}, status=400)
