###############################################################################
# Filename: ActiniaUser.py                                                     #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday June 6th 2022                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Nov 10 2023                                               #
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
# the Free Software Foundation, .either version 3 of the License, or           #
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
from django.db import models
from django.contrib.auth.models import BaseUserManager
from .ObjectAuditAbstract import ObjectAuditAbstract
from .fields.ActiniaRoleEnumField import ActiniaRoleEnumField
from .enums import RolesEnum
from django.conf import settings
from actinia import Actinia
from requests.auth import HTTPBasicAuth
from enum import Enum, unique
import requests
import json
import Location
import Mapset
import Token

# Actinia Super User Connection to create new users.
# Should make this role an admin
ACTINIA_SETTINGS = settings.ACTINIA
actinia_super_auth = HTTPBasicAuth(
    ACTINIA_SETTINGS["ACTINIA_USER"], ACTINIA_SETTINGS["ACTINIA_PASSWORD"]
)
actina_super_client = Actinia(
    os.path.join("http://", ACTINIA_SETTINGS["ACTINIA_BASEURL"]),
    ACTINIA_SETTINGS["ACTINIA_VERSION"],
)
actina_super_client.set_authentication(
    ACTINIA_SETTINGS["ACTINIA_USER"], ACTINIA_SETTINGS["ACTINIA_PASSWORD"]
)


@unique
class USER_TASK(Enum):
    USERS = "users"
    TOKEN = "token"
    API_KEY = "api_key"
    API_LOG = "api_log"


class ActiniaUser(ObjectAuditAbstract):
    """
    Custom user class to manage actinia user.

    Attributes:
        actinia_username (str): The username of the actinia user.
        actinia_role (ActiniaRoleEnumField): The role of the actinia user.
        user (ForeignKey): The related Django user object.
        password (str): The password of the actinia user.
    """

    __actinia_auth = None
    actinia_username = models.CharField(max_length=50, blank=False, unique=True)
    actinia_role = ActiniaRoleEnumField()
    user = models.ForeignKey(
        "auth.User", related_name="actinia_users", on_delete=models.CASCADE
    )
    password = models.CharField(max_length=128)

    def _auth(self):
        auth = HTTPBasicAuth(self.actinia_username, self.password)
        return auth

    def __base_url():
        # TODO: Add this full url to setting and enforce https
        ACTINIA_URL = os.path.join(
            "http://",
            ACTINIA_SETTINGS["ACTINIA_BASEURL"],
            "api",
            ACTINIA_SETTINGS["ACTINIA_VERSION"],
        )
        return ACTINIA_URL

    def __create_actinia_client(self):
        # TODO: Add this full url to setting and enforce https
        actinia_client = Actinia(
            os.path.join("http://", ACTINIA_SETTINGS["ACTINIA_BASEURL"]),
            ACTINIA_SETTINGS["ACTINIA_VERSION"],
        )
        actinia_client.set_authentication(self.actinia_username, self.password)
        self.__actinia_client = actinia_client
        return actinia_client

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
        base_url = f"{self.__base_url()}/{task}/"
        if user_id is not None:
            base_url = f"{base_url}/{user_id}"

        return base_url

    def actinia_version(self):
        """
        Get the version of the actinia instance.
        """
        return self.__actinia_client.get_version()

    def __generate_actinia_password(self):
        """
        Generate a password for managed actinia user.
        """
        new_password = BaseUserManager.make_random_password()
        self.password = new_password
        return self.password

    def generate_actinia_token(self):
        """
        Generate authorization token for user and store in Tokens
        """
        base_url = self.__base_url()
        Token.generate_actinia_token(base_url, self, api_key=True, expiration_time=None)

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

    def save(self, *args, **kwargs):
        """
        Create a new actinia user.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

    def __create_actinia_user(self):
        password = self.__generate_actinia_password()
        data = {"group": RolesEnum.USER, "password": password}

        url = self.__actinia_user_request_url(USER_TASK.USERS, self.actinia_username)

        try:
            response = requests.post(
                url,
                auth=actinia_super_auth,
                json=json.parse(data),
                headers={"content-type": "application/json; charset=utf-8"},
            )
            if response.status_code != 200:
                raise Exception(
                    f"Failed to make post request to {url}: {response.status_code}"
                )
        except Exception as e:
            print(e)
            raise

        client = self.__create_actinia_client()
        return client

    def create(self, epsg=3358):

        # Create new Actinia user
        actinia_client = self.__create_actinia_user()

        # Create defaut user location object
        location = actinia_client.create_location(self.actinia_username, epsg)

        # Create Mapset objects
        # TODO: Give Option to change default mapset name
        try:
            location.create_mapset("default")
        except Exception as e:
            print("Defautl mapset failed to be created: ", e)

        # Population users avaliable locations and mapsets
        locations = actinia_client.get_locations()
        self.__populate_locations_mapsets(locations)

    def __str__(self):
        """
        Return the actinia username.

        Returns:
            str: The actinia username.
        """
        return self.actinia_username

    class Meta:
        """
        Metadata for the ActiniaUser model.
        """

        ordering = ["created_on"]
        verbose_name = "Actinia User"
        verbose_name_plural = "Actinia Users"
        db_table = "actinia_users"
