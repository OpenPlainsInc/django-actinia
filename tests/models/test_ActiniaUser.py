###############################################################################
# Filename: test_ActiniaUser.py                                                #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday October 20th 2023                                       #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Aug 30 2024                                               #
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

from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from grass.models import ActiniaUser
from grass.models.enums import RolesEnum
from django.db import IntegrityError, transaction
from ..mocks.ActiniaUsersAPIMocks import ActiniaUsersAPIMocks


class ActiniaUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create(
            username="uesrtest1",
            email="uesrtest1@example.com",
            password="testpass",
        )

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_delete")
    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_post")
    def test_actinia_user_create_actinia_user(
        self, mock_users_user_id_post, mock_users_user_id_delete
    ):
        mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user(
            self.user.username
        )
        mock_users_user_id_delete.return_value = ActiniaUsersAPIMocks.delete_user(
            self.user.username
        )

        actinia_user = ActiniaUser.objects.create(
            user=self.user,
            actinia_username=self.user.username,
            actinia_role=RolesEnum.ADMIN.value,
        )

        # Assert that the actinia user is saved correctly
        self.assertEqual(actinia_user.actinia_username, "uesrtest1")
        self.assertEqual(actinia_user.actinia_role, RolesEnum.ADMIN.value)
        self.assertEqual(actinia_user.user, self.user)
        self.assertEqual(ActiniaUser.objects.count(), 1)
        # Delete the actinia user
        actinia_user.delete()
        self.assertEqual(ActiniaUser.objects.count(), 0)
        # Ensure the mock was called
        # mock_users_user_id_post.assert_called_once_with(user_id=self.user.username, password=actinia_user.password, group=RolesEnum.ADMIN.label)

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_post")
    def test_actinia_user_user_exists(self, mock_users_user_id_post):
        mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user_error(
            "test_user_id"
        )
        actinia_user = ActiniaUser.objects.create(
            user=self.user,
            actinia_username=self.user.username,
            actinia_role=RolesEnum.ADMIN.value,
        )

        with self.assertRaises(IntegrityError):
            ActiniaUser.objects.create(
                user=self.user,
                actinia_username=self.user.username,
                actinia_role=RolesEnum.ADMIN.value,
            )

            # End the transaction block before trying to delete the actinia user
            transaction.set_rollback(True)

            # Delete the actinia user
            actinia_user.delete()
            self.assertEqual(ActiniaUser.objects.count(), 0)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
