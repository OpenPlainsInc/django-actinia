###############################################################################
# Filename: test_ActiniaUser.py                                                #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday October 20th 2023                                       #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Wed Mar 06 2024                                               #
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


class ActiniaUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username="uesrtest1",
            email="uesrtest1@example.com",
            password="testpass",
        )

    def test_actinia_user_create_actinia_user(self):
        actinia_user = ActiniaUser.objects.create_actinia_user(self.user, "admin")

        # Assert that the actinia user is saved correctly
        self.assertEqual(actinia_user.actinia_username, "uesrtest1")
        self.assertEqual(actinia_user.actinia_role, "admin")
        self.assertEqual(actinia_user.user, self.user)
        self.assertEqual(ActiniaUser.objects.count(), 1)
        # Delete the actinia user
        actinia_user.delete()
        self.assertEqual(ActiniaUser.objects.count(), 0)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
