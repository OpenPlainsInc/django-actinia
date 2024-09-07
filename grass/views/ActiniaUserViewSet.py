###############################################################################
# Filename: ActiniaUserViewSet.py                                              #
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, routers
from grass.models import ActiniaUser
from grass.serializers import ActiniaUserResponseSerializer
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)


class ActiniaUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActiniaUser.objects.all()
    serializer_class = ActiniaUserResponseSerializer
    # http_method_names = ["get", "post", "delete"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        return self.serializer_class


class ActiniaUserDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            actinia_user = ActiniaUser.objects.get(pk=pk)
            serializer = ActiniaUserResponseSerializer(actinia_user)
            return Response(serializer.data)
        except ActiniaUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
