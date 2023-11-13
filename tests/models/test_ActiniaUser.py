###############################################################################
# Filename: test_ActiniaUser.py                                                #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday October 20th 2023                                       #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Nov 13 2023                                               #
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
from django.contrib.auth.models import User
from django.conf import settings
from grass.models import ActiniaUser
from requests.auth import HTTPBasicAuth
from actinia import Actinia

ACTINIA_SETTINGS = settings.ACTINIA


class ActiniaUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.actinia_user = ActiniaUser.objects.create(
            actinia_username="testuser",
            actinia_role="admin",
            user=self.user,
            password="testpass",
        )

    # def test_actinia_user_create_actinia_client(self):
    #     actinia_client = self.actinia_user._ActiniaUser__create_actinia_client()
    #     self.assertIsInstance(actinia_client, Actinia)
    #     self.assertEqual(actinia_client.base_url, self.actinia_user._ActiniaUser__base_url())
    #     self.assertEqual(actinia_client.version, ACTINIA_SETTINGS["ACTINIA_VERSION"])
    #     self.assertIsInstance(actinia_client.auth, HTTPBasicAuth)
    #     self.assertEqual(actinia_client.auth.username, self.actinia_user.actinia_username)
    #     self.assertEqual(actinia_client.auth.password, self.actinia_user.password)

    # def test_actinia_user_actinia_user_request_url(self):
    #     task = "test_task"
    #     url = self.actinia_user._ActiniaUser__actinia_user_request_url(task)
    #     self.assertIsInstance(url, str)
    #     self.assertIn(self.actinia_user._ActiniaUser__base_url(), url)
    #     self.assertIn(task, url)

    #     user_id = "test_user_id"
    #     url = self.actinia_user._ActiniaUser__actinia_user_request_url(task, user_id=user_id)
    #     self.assertIsInstance(url, str)
    #     self.assertIn(self.actinia_user._ActiniaUser__base_url(), url)
    #     self.assertIn(task, url)
    #     self.assertIn(user_id, url)

    # def test_actinia_user_actinia_version(self):
    #     version = self.actinia_user.actinia_version()
    #     self.assertIsInstance(version, str)
    #     self.assertGreater(len(version), 0)

    # def test_actinia_user_generate_actinia_password(self):
    #     password = self.actinia_user._ActiniaUser__generate_actinia_password()
    #     self.assertIsInstance(password, str)
    #     self.assertGreater(len(password), 0)
    #     self.assertNotEqual(password, self.actinia_user.password)

    # def test_actinia_user_generate_actinia_token(self):
    #     self.actinia_user.generate_actinia_token()
    #     self.assertIsNotNone(self.actinia_user.token)

    # def test_actinia_user_create(self):
    #     self.actinia_user.create()
    #     self.assertIsNotNone(self.actinia_user.actinia_username)
    #     self.assertIsNotNone(self.actinia_user.password)
    #     self.assertIsNotNone(self.actinia_user.user)
    #     self.assertIsNotNone(self.actinia_user.actinia_role)
    #     self.assertIsNotNone(self.actinia_user.token)
    #     self.assertIsNotNone(self.actinia_user._ActiniaUser__actinia_client)
    #     self.assertIsNotNone(self.actinia_user.locations())
    #     self.assertIsNotNone(self.actinia_user.teams())
    #     self.assertIsNotNone(self.actinia_user.projects())
    #     self.assertIsNotNone(self.actinia_user.grass_templates())

    def tearDown(self):
        self.actinia_user.delete()
        # self.user.delete()
        # ActiniaUser.objects.all().delete()
