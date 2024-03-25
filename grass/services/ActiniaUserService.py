###############################################################################
# Filename: ActiniaUserService.py                                              #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday November 13th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Mar 25 2024                                               #
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
from django.conf import settings
from grass.models.enums import RolesEnum
from requests.auth import HTTPBasicAuth
import logging
from grass.models import Token

import actinia_openapi_python_client
from actinia_openapi_python_client.rest import ApiException
from rest_framework import serializers
from django.http import JsonResponse
from grass.serializers import UserInfoResponseModelSerializer
from grass.serializers.UserListResponseSerializer import UserListResponseSerializer
from grass.serializers.ActiniaSimpleResponseSerializer import ResponseStatusSerializer


from django.db import transaction

ACTINIA_SETTINGS = settings.ACTINIA


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
            serializer = UserListResponseSerializer(data=api_response)
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
            serializer = UserInfoResponseModelSerializer(data=api_response)
            if serializer.is_valid():
                if serializer.data["status"] == "success":
                    self.logger.info(f"ActiniaUser retrieved: {user_id}")
                    return JsonResponse(serializer.data)
                else:
                    self.logger.error(
                        f"ActiniaUser retrieval failed: {serializer.data['message']}"
                    )
                    return JsonResponse(serializer.data)
        except ApiException as e:
            self.logger.error(
                f"Exception when calling UserManagementApi->users_user_id_get: {e}"
            )
            return JsonResponse({"error": str(e)}, status=400)

    def create_actinia_user(self, user, user_id, password, group=RolesEnum.USER.label):
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
            print(api_response)
            serializer = ResponseStatusSerializer(data=api_response)
            if serializer.is_valid():
                if serializer.data["status"] == "success":
                    self.logger.info(
                        f"ActiniaUser created: {user_id} in group: {group}"
                    )
                    return serializer.data
                else:
                    self.logger.error(
                        f"ActiniaUser creation failed: {serializer.data['message']}"
                    )
                    return JsonResponse(serializer.data, status=400)

        except ApiException as e:
            self.logger.error(
                f"Exception when calling UserManagementApi->users_user_id_post: {e}"
            )
            return JsonResponse({"error": str(e)}, status=400)

    def delete_actinia_user(self, actinia_username):
        """
        Deletes the actinia user for the user_id
        """
        try:
            actinia_user_id = actinia_username
            api_response = self.api_instance.users_user_id_delete(actinia_user_id)
            serializer = ResponseStatusSerializer(data=api_response)
            if serializer.is_valid():
                if serializer.data["status"] == "success":
                    self.logger.info(f"ActiniaUser deleted: {actinia_user_id}")
                    return serializer.data
                else:
                    self.logger.error(
                        f"ActiniaUser deletion failed: {serializer.data['message']}"
                    )
                    return serializer.data
        except ApiException as e:
            self.logger.error(
                f"Exception when calling UserManagementApi->users_user_id_delete: {e}"
            )
            return JsonResponse({"error": str(e)}, status=400)
