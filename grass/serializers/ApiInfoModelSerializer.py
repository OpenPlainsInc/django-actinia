###############################################################################
# Filename: ApiInfoModelSerializer.py                                          #
# Project: OpenPlains Inc.                                                     #
# File Created: Sunday December 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Sun Dec 17 2023                                               #
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


class ApiInfoModelSerializer(serializers.Serializer):
    """
    Serializer for Actinia API information model.
    Response schema that contains API information of the called endpoint.

    Attributes:
        endpoint (str): The endpoint that was called.
        method (str): The HTTP method that was used.
        path (str): The path of the called endpoint.
        request_url (str): The request URL of the called endpoint.
        post_url (str, optional): The POST URL of the called endpoint.
    """

    endpoint = serializers.CharField()
    method = serializers.CharField()  # TODO add enum of allowed methods
    path = serializers.CharField()
    request_url = serializers.URLField()
    post_url = serializers.URLField(required=False)
