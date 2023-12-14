###############################################################################
# Filename: MapsetInfoResponseSerializer.py                                    #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday November 21st 2023                                     #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Thu Dec 14 2023                                               #
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
    """
    Serializer for the ProcessLogModel class.

    Attributes:
        id (str): The ID of the process log.
        executable (str): The name of the executable.
        parameter (list): The list of parameters for the executable.
        stdout (str): The standard output of the process.
        stderr (list): The list of error messages from the process.
        return_code (float): The return code of the process.
        run_time (float, optional): The runtime of the process.
        mapset_size (float, optional): The size of the mapset.
    """

    id = serializers.CharField(required=False)
    executable = serializers.CharField()
    parameter = serializers.ListField(child=serializers.CharField())
    stdout = serializers.CharField()
    stderr = serializers.ListField(child=serializers.CharField())
    return_code = serializers.FloatField()
    run_time = serializers.FloatField(required=False)
    mapset_size = serializers.FloatField(required=False)


class OutputParameterMetadataSerializer(serializers.Serializer):
    format = serializers.CharField()


class OutputParameterExportSerializer(serializers.Serializer):
    """
    Serializer for the export output parameter.

    Attributes:
        format (str): The format of the export.
        type (str): The type of the export.
        dbstring (str, optional): The database connection string (if applicable).
        output_layer (str, optional): The output layer name (if applicable).
    """

    format = serializers.CharField()
    type = serializers.CharField()
    dbstring = serializers.CharField(required=False)
    output_layer = serializers.CharField(required=False)


class OutputParameterSerializer(serializers.Serializer):
    """
    Serializer for output parameters.

    Attributes:
        param (str): The parameter name.
        value (str): The parameter value.
        export (OutputParameterExportSerializer, optional): Serializer for export information (default: None).
        metadata (OutputParameterMetadataSerializer, optional): Serializer for metadata information (default: None).
    """

    param = serializers.CharField()
    value = serializers.CharField()
    export = OutputParameterExportSerializer(required=False)
    metadata = OutputParameterMetadataSerializer(required=False)


class StdoutParserSerializer(serializers.Serializer):
    """
    Serializer for parsing stdout response.

    Attributes:
        id (str): The ID of the response.
        format (str): The format of the response.
        delimiter (str): The delimiter used in the response.
    """

    id = serializers.CharField()
    format = serializers.CharField()
    delimiter = serializers.CharField()


class InputParameterImportDescrSerializer(serializers.Serializer):
    """
    Serializer for input parameters used in the import description.
    """

    type = serializers.CharField(required=False)
    sentinel_band = serializers.CharField(required=False)
    landsat_atcor = serializers.CharField(required=False)
    vector_layer = serializers.CharField(required=False)
    source = serializers.CharField(required=False)
    semantic_label = serializers.CharField(required=False)
    extent = serializers.CharField(required=False)
    filter = serializers.CharField(required=False)
    resample = serializers.CharField(required=False)
    resolution = serializers.CharField(required=False)
    resolution_value = serializers.CharField(required=False)
    basic_auth = serializers.CharField(required=False)


class InputParameterSerializer(serializers.Serializer):
    """
    Serializer for input parameters.

    Attributes:
        param (str): The parameter name.
        value (str): The parameter value.
        import_descr (InputParameterImportDescrSerializer, optional): The import description serializer.
    """

    param = serializers.CharField()
    value = serializers.CharField()
    import_descr = InputParameterImportDescrSerializer(required=False)


class GrassModuleSerializer(serializers.Serializer):
    """
    Serializer for GrassModule objects.

    Attributes:
        id (str): The ID of the GrassModule.
        module (str): The name of the GrassModule.
        inputs (list[InputParameterSerializer], optional): List of input parameters for the GrassModule.
        outputs (list[OutputParameterSerializer], optional): List of output parameters for the GrassModule.
        flags (str, optional): Additional flags for the GrassModule.
        stdin (str, optional): Standard input for the GrassModule.
        stdout (StdoutParserSerializer, optional): Serializer for parsing the standard output of the GrassModule.
        overwrite (bool, optional): Flag indicating whether to overwrite existing files.
        verbose (bool, optional): Flag indicating whether to display verbose output.
        superquiet (bool, optional): Flag indicating whether to suppress all output.
        interface_description (bool, optional): Flag indicating whether to display the interface description of the GrassModule.
    """

    id = serializers.CharField()
    module = serializers.CharField()
    inputs = InputParameterSerializer(many=True, required=False)
    outputs = OutputParameterSerializer(many=True, required=False)
    flags = serializers.CharField(required=False)
    stdin = serializers.CharField(required=False)
    stdout = StdoutParserSerializer(required=False)
    overwrite = serializers.BooleanField(required=False)
    verbose = serializers.BooleanField(required=False)
    superquiet = serializers.BooleanField(required=False)
    interface_description = serializers.BooleanField(required=False)


class MapsetInfoModelSerializer(serializers.Serializer):
    """
    Serializer for MapsetInfoModel.

    This serializer is used to serialize and deserialize MapsetInfoModel objects.
    It defines the fields that should be included in the serialized representation
    of a MapsetInfoModel instance.
    """

    projection = serializers.CharField()
    region = Region()


class ProgressInfoModelSerializer(serializers.Serializer):
    """
    Serializer for ProgressInfoModel.

    This serializer is used to serialize/deserialize ProgressInfoModel objects.
    It defines the fields and their types for the serialization process.
    """

    step = serializers.IntegerField()
    num_of_steps = serializers.IntegerField()
    sub_step = serializers.IntegerField(required=False)
    num_of_sub_steps = serializers.IntegerField(required=False)


class ExceptionTracebackModelSerializer(serializers.Serializer):
    """
    Serializer for representing exception traceback information.
    """

    message = serializers.CharField()
    type = serializers.CharField()
    traceback = serializers.ListField(child=serializers.CharField())


class UrlModelSerializer(serializers.Serializer):
    status = serializers.CharField()  # Add the status URL property
    resources = serializers.ListField(
        child=serializers.CharField()
    )  # Add the resources property


class ApiInfoModelSerializer(serializers.Serializer):
    """
    Serializer for API information model.
    """

    endpoint = serializers.CharField()
    method = serializers.CharField()
    path = serializers.CharField()
    request_url = serializers.CharField()
    post_url = serializers.CharField(required=False)


class MapsetInfoResponseModelSerializer(serializers.Serializer):
    """
    Serializer for MapsetInfoResponseModel.

    This serializer is used to serialize and deserialize MapsetInfoResponseModel objects.
    It defines the fields and their types for the serialization process.
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
