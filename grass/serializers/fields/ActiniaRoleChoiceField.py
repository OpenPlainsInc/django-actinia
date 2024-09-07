###############################################################################
# Filename: ActiniaRoleChoiceField.py                                          #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday September 2nd 2024                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Sep 02 2024                                               #
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
from grass.models.enums.RolesEnum import RolesEnum


class ActiniaRoleChoiceField(serializers.ChoiceField):
    """
    Custom serializer to handle Actinia resource response statuses.
    (superadmin, admin, user, guest)
    """

    def __init__(self, **kwargs):
        kwargs["choices"] = RolesEnum.choices
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
