###############################################################################
# Filename: EnumChoiceField.py                                                 #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday September 3rd 2024                                     #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Sep 03 2024                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2024 OpenPlains Inc.                                           #
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


class EnumChoiceField(serializers.ChoiceField):
    def __init__(self, enum_class, **kwargs):
        self.enum_class = enum_class
        choices = [(tag.value, tag.label) for tag in enum_class]
        super().__init__(choices=choices, **kwargs)

    def to_representation(self, obj):
        # Convert the value to the human-readable label in the response
        if obj in self.choices:
            return self.choices[obj]
        return obj

    def to_internal_value(self, data):
        # Validate and convert the input to the enum value
        if data in self.choices:
            return data
        self.fail("invalid_choice", input=data)
