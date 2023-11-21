###############################################################################
# Filename: MapsetInfoResponseSerializer.py                                    #
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

from rest_framework import serializers
from grass.models.Region import Region


class ProcessLogModelSerializer(serializers.Serializer):
    # Define the fields for the ProcessLogModel
    # ...
    pass


class GrassModuleSerializer(serializers.Serializer):
    # Define the fields for the GrassModule
    # ...
    pass


class MapsetInfoModelSerializer(serializers.Serializer):
    # projection 	str 	The location projection WKT string
    # region 	RegionModel
    projection = serializers.CharField()
    region = Region()


class ProgressInfoModelSerializer(serializers.Serializer):
    # step 	int 	The current processing step
    # num_of_steps 	int 	The total number of processing steps
    # sub_step 	int 	The current sub step of the current processing step 	[optional]
    # num_of_sub_steps 	int 	The total number of sub steps of the current processing step 	[optional]
    step = serializers.IntegerField()
    num_of_steps = serializers.IntegerField()
    sub_step = serializers.IntegerField(required=False)
    num_of_sub_steps = serializers.IntegerField(required=False)


class ExceptionTracebackModelSerializer(serializers.Serializer):
    message = serializers.CharField()
    type = serializers.CharField()
    traceback = serializers.ListField(child=serializers.CharField())


class UrlModelSerializer(serializers.Serializer):
    status = serializers.CharField()  # Add the status URL property
    resources = serializers.ListField(
        child=serializers.CharField()
    )  # Add the resources property


class ApiInfoModelSerializer(serializers.Serializer):
    endpoint = serializers.CharField()
    method = serializers.CharField()
    path = serializers.CharField()
    request_url = serializers.CharField()
    post_url = serializers.CharField(required=False)


class MapsetInfoResponseModelSerializer(serializers.Serializer):
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
