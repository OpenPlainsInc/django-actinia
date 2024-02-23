###############################################################################
# Filename: ActiniaWebhookFinishedReceiver.py                                  #
# Project: OpenPlains Inc.                                                     #
# File Created: Wednesday December 27th 2023                                   #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Wed Dec 27 2023                                               #
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from grass.serializers.ProcessingResponseSerializer import ProcessingResponseSerializer


class ActiniaWebhookFinishedReceiver(APIView):
    def post(self, request, *args, **kwargs):
        # Handle incoming webhook payload here
        payload = request.data

        # Process the payload (e.g., save to database, trigger actions)
        # ...
        serializer = ProcessingResponseSerializer(data=payload)
        if serializer.is_valid():
            # Syncroniztion events
            # * Create a new actinia user
            # * Create a new actinia location
            # * Create a new actinia mapset
            # * Add a new actinia layer to mapset
            # * Update a layer in mapset
            # * Update a mapset
            # * Update a location
            # * Delete a layer from mapset
            # * Delete a mapset
            # * Delete a location
            # * Delete a user
            # * Execute a process

            # serializer.save()
            return Response(
                {"message": "Webhook received successfully"}, status=status.HTTP_200_OK
            )
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
