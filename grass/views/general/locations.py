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
from grass.serializers import LocationSerializer, LocationDetailSerializer
from grass.serializers.LocationDetailSerializer import (
    extract_bbox_from_wkt,
    extract_unit_from_wkt,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import logging

logger = logging.getLogger(__name__)


class LocationViewSet(viewsets.ModelViewSet):
    """
    List all locations, or create a new location.
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific location enriched with Actinia location info.

        In addition to the standard model fields the response includes:
        - ``region``: current computational region from Actinia
        - ``bbox``: bounding box parsed from the CRS WKT
        - ``unit``: linear/angular unit parsed from the CRS WKT
        - ``mapsets``: names of mapsets that belong to this location
        """
        from grass.services.ProjectService import ProjectService

        location = self.get_object()
        serializer = LocationDetailSerializer(location, context={"request": request})
        data = dict(serializer.data)

        region = None
        bbox = None
        unit = None
        try:
            project_service = ProjectService()
            actinia_data = project_service.get_project(location.name)
            if actinia_data and "process_results" in actinia_data:
                process_results = actinia_data["process_results"]
                region = process_results.get("region")
                projection_wkt = process_results.get("projection", "")
                bbox = extract_bbox_from_wkt(projection_wkt)
                unit = extract_unit_from_wkt(projection_wkt)
        except Exception as e:
            logger.warning(
                "Could not retrieve Actinia location info for %s: %s",
                location.name,
                e,
            )

        data["region"] = region
        data["bbox"] = bbox
        data["unit"] = unit
        data["mapsets"] = list(location.mapsets.values_list("name", flat=True))
        return Response(data)

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
