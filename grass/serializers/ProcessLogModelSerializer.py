###############################################################################
# Filename: ProcessLogModelSerializer.py                                       #
# Project: OpenPlains Inc.                                                     #
# File Created: Sunday December 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Sep 02 2024                                               #
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


class ProcessLogModelSerializer(serializers.Serializer):
    """
    Serializer for the ProcessLogModel class.

    Attributes:
        id (str): The ID of the executable.
        executable (str): The name of the executable.
        parameter (list): The parameter of the executable.
        stdout (str): The stdout output of the executable.
        stderr (list): The stderr output of the executable as list of strings.
        return_code (float): The return code of the executable.
        run_time (float, optional): The runtime of the executable in seconds.
        mapset_size (float, optional): The size of the mapset in bytes.
    """

    id = serializers.CharField(required=False)
    executable = serializers.CharField()
    parameter = serializers.ListField(child=serializers.CharField())
    stdout = serializers.CharField(required=False, allow_blank=True)
    stderr = serializers.ListField(
        child=serializers.CharField(required=False, allow_blank=True),
        required=False,
        default=[],
    )
    return_code = serializers.FloatField()
    run_time = serializers.FloatField(required=False)
    mapset_size = serializers.FloatField(required=False)
