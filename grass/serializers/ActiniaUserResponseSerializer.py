###############################################################################
# Filename: ActiniaUserResponseSerializer.py                                   #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday November 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Sep 02 2024                                               #
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
from grass.serializers.LocationSerializer import LocationSerializer
from grass.models import ActiniaUser
from .fields import ActiniaRoleChoiceField
from grass.services import ActiniaUserService

# from grass.serializers.UserInfoResponseModelSerializer import UserInfoResponseModelSerializer
import logging

logger = logging.getLogger(__name__)


class ActiniaUserResponseSerializer(serializers.Serializer):
    """
    Serializer for ActiniaUserResponse objects.
    """

    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    actinia_username = serializers.CharField()
    actinia_role = ActiniaRoleChoiceField()
    locations = LocationSerializer(many=True, read_only=True)
    created_on = serializers.DateTimeField()
    updated_on = serializers.DateTimeField()
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = "ActiniaUser"
        fields = "__all__"
        depth = 1

    def get_user_details(self, obj):
        """Get the user details for the actinia user"""
        try:
            actinia_user_service = ActiniaUserService.ActiniaUserService()
            user_details = actinia_user_service.get_actinia_user(obj.actinia_username)
            logger.info(f"User Details for {obj.actinia_username}: {user_details}")
            return user_details
        except Exception as e:
            logger.error(f"Error fetching user details: {e}")
            return {"error": "Error fetching user details"}
