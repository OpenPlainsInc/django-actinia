###############################################################################
# Filename: ProcessingResponseSerializer.py                                    #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday November 21st 2023                                     #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Nov 21 2023                                               #
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

# Properties
# Name 	Type 	Description 	Notes
# status 	str 	The status of the response
# user_id 	str 	The id of the user that issued a request
# resource_id 	str 	The unique resource id
# queue 	str 	The name of the queue in which the job is queued 	[optional]
# process_log 	List[ProcessLogModel] 	A list of ProcessLogModels 	[optional]
# process_chain_list 	List[GrassModule] 	The list of GRASS modules that were used in the processing 	[optional]
# process_results 	str 	An arbitrary class that stores the processing results 	[optional]
# progress 	ProgressInfoModel 		[optional]
# message 	str 	Message for the user, maybe status, finished or error message
# exception 	ExceptionTracebackModel 		[optional]
# accept_timestamp 	float 	The acceptance timestamp in seconds of the response
# accept_datetime 	str 	The acceptance timestamp of the response in human readable format
# timestamp 	float 	The current timestamp in seconds of the response
# time_delta 	float 	The time delta of the processing in seconds 	[optional]
# datetime 	str 	The current timestamp of the response in human readable format
# http_code 	float 	The HTTP code of the response 	[optional]
# urls 	UrlModel 		[optional]
# api_info 	ApiInfoModel 		[optional]


class ProcessingResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for ProcessingResponse objects.
    """

    process_log = serializers.ListField(child=serializers.DictField(), required=False)
    process_chain_list = serializers.ListField(
        child=serializers.DictField(), required=False
    )
    progress = serializers.DictField(required=False)
    exception = serializers.DictField(required=False)
    time_delta = serializers.FloatField(required=False)
    urls = serializers.DictField(required=False)
    api_info = serializers.DictField(required=False)

    class Meta:
        model = ProcessingResponseModel
        fields = [
            "status",
            "user_id",
            "resource_id",
            "queue",
            "process_log",
            "process_chain_list",
            "process_results",
            "progress",
            "message",
            "exception",
            "accept_timestamp",
            "accept_datetime",
            "timestamp",
            "time_delta",
            "datetime",
            "http_code",
            "urls",
            "api_info",
        ]
