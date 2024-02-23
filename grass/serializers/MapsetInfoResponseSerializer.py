###############################################################################
# Filename: MapsetInfoResponseSerializer.py                                    #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday November 21st 2023                                     #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Thu Jan 11 2024                                               #
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

from .MapsetInfoModelSerializer import MapsetInfoModelSerializer
from .ProgressInfoModelSerializer import ProgressInfoModelSerializer
from .UrlModelSerializer import UrlModelSerializer
from .ApiInfoModelSerializer import ApiInfoModelSerializer
from .ProcessLogModelSerializer import ProcessLogModelSerializer
from .GrassModuleSerializer import GrassModuleSerializer
from .ExceptionTracebackModelSerializer import ExceptionTracebackModelSerializer


class MapsetInfoResponseSerializer(serializers.Serializer):
    """
    Serializer for MapsetInfoResponseModel.

    This serializer is used to serialize and deserialize MapsetInfoResponseModel objects.
    It defines the fields and their types for the serialization process.

    Attributes:
        status (str): The status of the response.
        user_id (str): The id of the user that issued a request.
        resource_id (str): The unique resource id.
        queue (str, optional): The name of the queue in which the job is queued.
        process_log (List[ProcessLogModel], optional): A list of ProcessLogModels.
        process_chain_list (List[GrassModule], optional): The list of GRASS modules that were used in the processing.
        process_results (MapsetInfoModel, optional).
        progress (ProgressInfoModel, optional).
        message (str): Message for the user, maybe status, finished or error message.
        exception (ExceptionTracebackModel, optional).
        accept_timestamp (float): The acceptance timestamp in seconds of the response.
        accept_datetime (str): The acceptance timestamp of the response in human readable format.
        timestamp (float): The current timestamp in seconds of the response.
        time_delta (float, optional): The time delta of the processing in seconds.
        datetime (str): The current timestamp of the response in human readable format.
        http_code (float, optional): The HTTP code of the response.
        urls (UrlModel, optional).
        api_info (ApiInfoModel, optional).
    """

    status = serializers.CharField()
    user_id = serializers.CharField()
    resource_id = serializers.CharField()
    queue = serializers.CharField(required=False)
    process_log = ProcessLogModelSerializer(many=True, required=False)
    process_chain_list = GrassModuleSerializer(many=True, required=False)
    process_results = MapsetInfoModelSerializer(required=False)
    progress = ProgressInfoModelSerializer(required=False)
    message = serializers.CharField()
    exception = ExceptionTracebackModelSerializer(required=False)
    accept_timestamp = serializers.FloatField()
    accept_datetime = serializers.CharField()
    timestamp = serializers.FloatField()
    time_delta = serializers.FloatField(required=False)
    datetime = serializers.CharField()
    http_code = serializers.FloatField(required=False)
    urls = UrlModelSerializer(required=False)
    api_info = ApiInfoModelSerializer(required=False)
