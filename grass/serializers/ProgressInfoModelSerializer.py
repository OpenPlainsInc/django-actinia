###############################################################################
# Filename: ProgressInfoModelSerializer.py                                     #
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


class ProgressInfoModelSerializer(serializers.Serializer):
    """
    Serializer for ProgressInfoModel.

    This serializer is used to serialize/deserialize ProgressInfoModel objects.
    It defines the fields and their types for the serialization process.

    Attributes:
        step (int): The current processing step.
        num_of_steps (int): The total number of processing steps.
        sub_step (int, optional): The current sub step of the current processing step.
        num_of_sub_steps (int, optional): The total number of sub steps of the current processing step.
    """

    step = serializers.IntegerField()
    num_of_steps = serializers.IntegerField()
    sub_step = serializers.IntegerField(required=False)
    num_of_sub_steps = serializers.IntegerField(required=False)
