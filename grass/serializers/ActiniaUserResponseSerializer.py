###############################################################################
# Filename: ActiniaUserResponseSerializer.py                                   #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday November 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Thu Mar 21 2024                                               #
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


class ActiniaUserResponseSerializer(serializers.Serializer):
    """
    Serializer for ActiniaUserResponse objects.
    """

    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    actinia_username = serializers.CharField()
    actinia_role = serializers.CharField()
    locations = LocationSerializer(many=True, read_only=True)
    created_on = serializers.DateTimeField()
    updated_on = serializers.DateTimeField()
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    # modules = serializers.JSONField()

    class Meta:
        model = "ActiniaUser"
        fields = "__all__"
        depth = 1
