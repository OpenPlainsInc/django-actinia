###############################################################################
# Filename: LocationSerializer.py                                              #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday June 7th 2022                                          #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Sep 03 2024                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2023 OpenPlains Inc.                                                #
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
from grass.models import Location, ActiniaUser

# User = get_user_model()


class LocationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    actinia_users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ActiniaUser.objects.all(), required=False
    )

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "epsg",
            "public",
            "slug",
            "actinia_users",
            "created_on",
            "created_by",
            "updated_on",
            "updated_by",
        ]
        read_only_fields = [
            "id",
            "slug",
            "created_on",
            "updated_on",
            "created_by",
            "updated_by",
            "owner",
        ]

    def save(self, **kwargs):
        # Pass the owner to the save method via kwargs if it's not set
        kwargs["owner"] = self.context["request"].user
        location = super().save(**kwargs)

        # Check if actinia_users is empty
        if not self.validated_data.get("actinia_users"):
            # Get the current user from the context
            user = self.context["request"].user

            # Get the ActiniaUser instance corresponding to the current user
            actinia_user = ActiniaUser.objects.get(user=user)

            # Add the user's ActiniaUser instance to the actinia_users field
            location.actinia_users.add(actinia_user)

        return location
