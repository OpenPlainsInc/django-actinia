###############################################################################
# Filename: locations.py                                                       #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday June 6th 2022                                           #
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

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from grass.models import Location
from grass.serializers import LocationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class LocationViewSet(viewsets.ModelViewSet):
    """
    List all locations, or create a new location.
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    @action(detail=True, methods=["get"])
    def custom_action(self, request, pk=None):
        """
        Custom action for retrieving a specific location.
        """
        location = self.get_object()
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    # def create(self, request):
    #     """
    #     Create a new location.
    #     """
    #     serializer = LocationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """
        Set the updated_by field during update.
        """
        serializer.save(updated_by=self.request.user)

    # def update(self, request, pk=None):
    #     """
    #     Update a location.
    #     """
    #     location = self.get_object()
    #     serializer = LocationSerializer(location, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(updated_by=self.request.user)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, pk=None):
    #     """
    #     Partially update a location.
    #     """
    #     location = self.get_object()
    #     serializer = LocationSerializer(location, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save(updated_by=self.request.user)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete a location.
        """
        location = self.get_object()
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
