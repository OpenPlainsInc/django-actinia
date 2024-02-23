###############################################################################
# Filename: test_ActiniaUser.py                                                #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday October 20th 2023                                       #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Nov 20 2023                                               #
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
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from grass.models import ActiniaUser, Location, Mapset, Token
from requests.auth import HTTPBasicAuth
from actinia import Actinia
from django.db.models.query import QuerySet

# import requests_mock
import time


ACTINIA_SETTINGS = settings.ACTINIA

ACTINIA_URL = os.path.join(
    ACTINIA_SETTINGS["ACTINIA_BASEURL"],
    "api",
    ACTINIA_SETTINGS["ACTINIA_VERSION"],
)


class ActiniaUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username="actiniatestuser",
            email="testuser@example.com",
            password="testpass",
        )

        cls.actinia_user = ActiniaUser.create_actinia_user(cls.user, "admin")

    def test_actinia_user_str(self):
        self.assertEqual(str(self.actinia_user), "actiniatestuser")

    # Test that the ActiniaUser object is created correctly
    def test_actinia_user_create(self):
        self.assertEqual(self.actinia_user.actinia_username, "actiniatestuser")
        self.assertEqual(self.actinia_user.actinia_role, "admin")
        self.assertEqual(self.actinia_user.user, self.user)

    # Test that creating an ActiniaUser object with an existing username raises an exception
    # def test_actinia_user_failed_to_create_user(self):
    #     with self.assertRaises(Exception):
    #         ActiniaUser.objects.create(
    #             actinia_username="testuser",
    #             actinia_role="admin",
    #             user=self.user
    #         )

    # def test_manual_create_actinia_user(self):
    #     with self.assertRaises(Exception):
    #         test_actinia_user = self.actinia_user._ActiniaUser__create_actinia_user()
    #         self.assertIsInstance(test_actinia_user, Actinia)

    # def test_actinia_base_url(self):
    #     base_url = self.actinia_user._ActiniaUser__base_url
    #     self.assertEqual(base_url, ACTINIA_URL)

    # def test_actinia_user_request_url(self):
    #     task = "users"
    #     url = self.actinia_user._ActiniaUser__actinia_user_request_url(task)
    #     self.assertIsInstance(url, str)
    #     self.assertIn(self.actinia_user._ActiniaUser__base_url, url)
    #     self.assertIn(task, url)

    #     user_id = "test_user_id"
    #     url = self.actinia_user._ActiniaUser__actinia_user_request_url(task, user_id=user_id)
    #     self.assertIsInstance(url, str)
    #     self.assertIn(self.actinia_user._ActiniaUser__base_url, url)
    #     self.assertIn(task, url)
    #     self.assertIn(user_id, url)

    #     task = "token"
    #     url = self.actinia_user._ActiniaUser__actinia_user_request_url(task)
    #     self.assertIsInstance(url, str)
    #     self.assertIn(self.actinia_user._ActiniaUser__base_url, url)
    #     self.assertIn(task, url)

    #     task = "api_key"
    #     url = self.actinia_user._ActiniaUser__actinia_user_request_url(task)
    #     self.assertIsInstance(url, str)
    #     self.assertIn(self.actinia_user._ActiniaUser__base_url, url)
    #     self.assertIn(task, url)

    #     task = "api_log"
    #     url = self.actinia_user._ActiniaUser__actinia_user_request_url(task)
    #     self.assertIsInstance(url, str)
    #     self.assertIn(self.actinia_user._ActiniaUser__base_url, url)
    #     self.assertIn(task, url)

    #     with self.assertRaises(Exception):
    #         task = "fake_task"
    #         url = self.actinia_user._ActiniaUser__actinia_user_request_url(task)

    # def test_actina_user_create_actinia_client(self):
    #     actinia_client = self.actinia_user._ActiniaUser__create_actinia_client()
    #     self.assertIsInstance(actinia_client, Actinia)
    #     actinia_client_auth = self.actinia_user._ActiniaUser__auth
    #     self.assertIsInstance(actinia_client_auth, HTTPBasicAuth)

    # def test_actina_user_default_location_creation(self):
    #     locations_count = self.actinia_user.locations.count()
    #     locations = self.actinia_user.locations.all()

    #     self.assertIsInstance(locations, QuerySet)
    #     self.assertEqual(locations_count, 0)

    @classmethod
    def tearDownClass(cls):
        # Clean up any resources that were created in the setUpTestData() classmethod or by the test methods
        # cls.actinia_user.objects.delete()
        ActiniaUser.objects.delete_actinia_user(cls.actinia_user)
        cls.user.delete()
