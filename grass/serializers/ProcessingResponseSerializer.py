###############################################################################
# Filename: ProcessingResponseSerializer.py                                    #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday November 21st 2023                                     #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Aug 30 2024                                               #
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

from actinia_openapi_python_client.models.processing_response_model import (
    ProcessingResponseModel,
)
from rest_framework import serializers
from .fields.ResourceStatusChoiceField import ResourceStatusChoiceField


class ProcessingResponseSerializer(serializers.Serializer):
    """
    Serializer for ProcessingResponse objects.
    """

    status = ResourceStatusChoiceField(required=True)
    user_id = serializers.CharField(required=True)
    resource_id = serializers.CharField(required=True)
    queue = serializers.CharField(required=False)
    process_log = serializers.ListField(child=serializers.DictField(), required=False)
    process_chain_list = serializers.ListField(
        child=serializers.DictField(), required=False
    )
    process_results = serializers.DictField(required=False)
    progress = serializers.DictField(required=False)
    exception = serializers.DictField(required=False)
    accept_timestamp = serializers.FloatField(required=False)
    accept_datetime = serializers.CharField(required=False)
    timestamp = serializers.FloatField(required=False)
    time_delta = serializers.FloatField(required=False)
    datetime = serializers.CharField(required=False)
    http_code = serializers.IntegerField(required=False)
    urls = serializers.DictField(required=False)
    api_info = serializers.DictField(required=False)
    message = serializers.CharField(required=False)
