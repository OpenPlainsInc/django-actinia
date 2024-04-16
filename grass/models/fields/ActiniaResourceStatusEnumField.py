###############################################################################
# Filename: ActiniaResourceStatusEnumField.py                                  #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday June 7th 2022                                          #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Sat Apr 13 2024                                               #
# Modified By: Srihitha Reddy Kaalam                                           #
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

from grass.models.enums import ResourceStatusEnum
from django.db import models


class ActiniaResourceStatusEnumField(models.CharField):
    """
    A custom model field for actinia user roles. This field extends CharField and
    uses a ResourceStatusEnum for the choices and a default value.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 10)
        kwargs.setdefault("choices", ResourceStatusEnum.choices)
        kwargs.setdefault("default", ResourceStatusEnum.ACCEPTED)
        super().__init__(*args, **kwargs)
