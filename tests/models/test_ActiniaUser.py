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
from actinia.models import ActiniaUser


class ActiniaUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.actinia_user = ActiniaUser.objects.create(
            actinia_username="testactiniauser",
            actinia_role="admin",
            user=self.user,
            password="testpass",
        )

    def test_actinia_user_str(self):
        self.assertEqual(str(self.actinia_user), "testactiniauser")

    def test_actinia_user_password(self):
        self.assertNotEqual(self.actinia_user.password, "testpass")

    def test_actinia_user_generate_token(self):
        self.actinia_user.generateActiniaToken()
        self.assertIsNotNone(self.actinia_user.token)

    def test_actinia_user_locations(self):
        self.assertEqual(self.actinia_user.locations(), [])

    def test_actinia_user_projects(self):
        self.assertEqual(self.actinia_user.projects(), [])

    def test_actinia_user_grass_templates(self):
        self.assertEqual(self.actinia_user.grass_templates(), [])

    def test_actinia_user_create(self):
        self.actinia_user.create()
        self.assertIsNotNone(self.actinia_user.actinia_username)
        self.assertIsNotNone(self.actinia_user.password)
        self.assertIsNotNone(self.actinia_user.user)
        self.assertIsNotNone(self.actinia_user.actinia_role)
        self.assertIsNotNone(self.actinia_user.token)
        self.assertIsNotNone(self.actinia_user.__actinia_client)
        self.assertIsNotNone(self.actinia_user.locations())
        self.assertIsNotNone(self.actinia_user.teams())
        self.assertIsNotNone(self.actinia_user.projects())
        self.assertIsNotNone(self.actinia_user.grass_templates())
