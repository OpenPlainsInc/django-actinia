###############################################################################
# Filename: mapsets.py                                                         #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday June 6th 2022                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Thu Jan 11 2024                                               #
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

# create an APIView for the Mapset model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from grass.models.Mapset import Mapset
from grass.serializers.MapsetResponseModelSerializer import (
    MapsetResponseModelSerializer,
)
from grass.serializers.MapsetInfoModelSerializer import MapsetInfoModelSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny


class MapsetViewSet(viewsets.ViewSet):
    """
    List all Mapsets, or create a new Mapset.
    """

    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Mapset.objects.all()
        serializer = MapsetInfoModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        queryset = Mapset.objects.all()
        location = get_object_or_404(queryset, pk=pk)
        serializer = MapsetInfoModelSerializer(location)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
