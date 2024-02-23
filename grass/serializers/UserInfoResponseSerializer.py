###############################################################################
# Filename: UserInfoResponseSerializer.py                                      #
# Project: OpenPlains Inc.                                                     #
# File Created: Wednesday November 15th 2023                                   #
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

from rest_framework import serializers

from actinia_openapi_python_client.models.user_info_response_model_permissions import (
    UserInfoResponseModelPermissions,
)


class UserInfoResponseModelPermissionsSerializer(serializers.Serializer):
    cell_limit = serializers.IntegerField(required=False, allow_null=True)
    process_num_limit = serializers.IntegerField(required=False, allow_null=True)
    process_time_limit = serializers.CharField(required=False, allow_null=True)
    accessible_datasets = serializers.JSONField(required=False, allow_null=True)
    accessible_modules = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )


class UserInfoResponseModelSerializer(serializers.Serializer):
    status = serializers.CharField()
    user_id = serializers.CharField(required=False, allow_null=True)
    user_role = serializers.CharField(required=False, allow_null=True)
    user_group = serializers.CharField(required=False, allow_null=True)
    permissions = UserInfoResponseModelPermissionsSerializer(
        required=False, allow_null=True
    )
