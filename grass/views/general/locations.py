###############################################################################
# Filename: locations.py                                                       #
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

# from html5lib import serialize
import requests
import grass.utils as acp
from django.http import JsonResponse
from grass.models import Location
from grass.serializers import LocationSerializer, LocationResponseSerializer

# from actinia.serializers.LocationResponseSerializer import LocationResponseSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny


# def gLocations(request):
#     """
#     Gets List of Users Avaliable Locations
#     Actinia Route
#     GET /locations
#     """
#     if request.method == "GET":
#         url = f"{acp.baseUrl()}/locations"
#         r = requests.get(url, auth=acp.auth())
#         print(f"Request URL: {url}")
#         serializer = LocationResponseSerializer(r.json())
#         return Response(serializer.data)
#     # TODO - Set up proper error handling and reponse messages
#     return JsonResponse({"error": "gLocations View: Fix Me"})


# class LocationList(APIView):
#     """
#     List all of the users locations or create a new location.
#     """


#     def get(self, request, format=None):
#         locations = Location.object.all()
#         serializer = LocationSerializer(locations, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = LocationSerializer(request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LocationDetail(APIView):
#     """Retrieve, update or delete a location instance."""

#     def get_object(self, location_id):
#         try:
#             return Location.objects.get(id=location_id)
#         except Location.DoesNotExist:
#             raise Http404

#     def get(self, request, location_id, format=None):
#         location = self.get_object(location_id)
#         serializer = LocationSerializer(location)
#         return Response(serializer.data)

#     def put(self, request, location_id, format=None):
#         location = self.get_object(location_id)
#         serializer = LocationSerializer(location, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, location_id, format=None):
#         location = self.get_object(location_id)
#         location.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class LocationViewSet(viewsets.ViewSet):
    """
    List all locations,
    or create a new location.
    """

    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        queryset = Location.objects.all()
        location = get_object_or_404(queryset, pk=pk)
        serializer = LocationResponseSerializer(location)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
