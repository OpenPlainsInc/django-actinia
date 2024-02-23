###############################################################################
# Filename: LayerTypeEnum.py                                                   #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday November 27th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Wed Dec 27 2023                                               #
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

from django.db import models
from django.utils.translation import gettext_lazy as _


class LayerTypeEnum(models.TextChoices):
    """
    Enum class representing the different layer types.
    """

    RASTER = "RS", _("raster")
    RASTER_3D = "R3", _("raster_3d")
    VECTOR = "VE", _("vector")
    STDR = "ST", _("stdr")
    STAC = "SC", _("stac")
    TABULAR = "TA", _("tabular")
