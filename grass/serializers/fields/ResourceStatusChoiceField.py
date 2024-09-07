###############################################################################
# Filename: ResourceStatusChoiceField.py                                       #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday June 7th 2022                                          #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Sep 03 2024                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2023 OpenPlains Inc.                                                #
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
from grass.models.enums.ResourceStatusEnum import ResourceStatusEnum


class ResourceStatusChoiceField(serializers.ChoiceField):
    """
    Custom serializer to handle Actinia resource response statuses.
    (accepted, running, finished, terminated, error)
    """

    def __init__(self, **kwargs):
        kwargs["choices"] = ResourceStatusEnum.choices
        kwargs["allow_blank"] = False
        super().__init__(**kwargs)

    def to_representation(self, value):
        """Converts the internal value to the string representation of a choice."""
        if value in ("", None):
            return value
        return self.choices[value]

    def to_internal_value(self, data):
        """Converts the string representation of a choice to the internal value."""
        for key, label in self.choices.items():
            if data == label:
                return key
        self.fail("invalid_choice", input=data)
