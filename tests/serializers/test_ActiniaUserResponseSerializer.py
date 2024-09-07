###############################################################################
# Filename: test_ActiniaUserResponseSerializer.py                              #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday November 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Sep 06 2024                                               #
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


from django.test import TransactionTestCase
from grass.serializers import (
    ActiniaUserResponseSerializer,
)
from grass.models.enums import RolesEnum
from grass.models.ActiniaUser import ActiniaUser
from unittest.mock import patch
from ..mocks.ActiniaUsersAPIMocks import ActiniaUsersAPIMocks

# from django.db import transaction
from rest_framework.exceptions import ValidationError
from grass.serializers.fields import ActiniaRoleChoiceField
from grass.services import ActiniaUserService

from django.contrib.auth import get_user_model


User = get_user_model()


class ActiniaUserResponseSerializerTestCase(TransactionTestCase):
    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_post")
    def setUp(self, mock_users_user_id_post):

        mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user(
            "testuser"
        )

        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )

        self.user_data = {
            "id": self.user.id,
            "user_id": self.user.id,
            "actinia_username": self.user.username,
            "actinia_role": RolesEnum.ADMIN.label,
            "projects": [],
            "created_on": "2023-11-17T00:00:00Z",
            "updated_on": "2023-11-17T00:00:00Z",
            "created_by": self.user.get_username(),
            "updated_by": self.user.get_username(),
            "user_details": {},
        }

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_get")
    def test_serializer_valid(self, mock_users_user_id_get):

        mock_users_user_id_get.return_value = ActiniaUsersAPIMocks.get_user(
            self.user.username, as_dict=False
        )

        serializer = ActiniaUserResponseSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
