###############################################################################
# Filename: LayerTypeEnumField.py                                              #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday November 27th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Mar 22 2024                                               #
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

from grass.models.enums import LayerTypeEnum
from django.db import models
from django.utils.translation import gettext_lazy as _


class LayerTypeEnumField(models.CharField):
    """
    Custom model field for GRASS layer types
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 2)
        kwargs.setdefault("choices", LayerTypeEnum.choices)
        kwargs.setdefault("default", LayerTypeEnum.RASTER)
        super().__init__(*args, **kwargs)
