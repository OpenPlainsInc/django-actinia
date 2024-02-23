###############################################################################
# Filename: Layer.py                                                           #
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
from .ObjectAuditAbstract import ObjectAuditAbstract
from .ObjectInfoAbstract import ObjectInfoAbstract
from .Mapset import Mapset
from .fields.LayerTypeEnumField import LayerTypeEnumField


class Layer(ObjectAuditAbstract, ObjectInfoAbstract):
    """
    GRASS Layer class
    """

    mutable = models.BooleanField(default=False)
    mapsets = models.ManyToManyField("grass.Mapset", related_name="layers")
    users = models.ManyToManyField("grass.User", related_name="layers")
    layer_type = LayerTypeEnumField()
    size = models.CharField()  # KB
    eres = models.FloatField()
    wres = models.FloatField()
    stac_asset = models.URLField()
    thumbnail = models.URLField()
    bbox = models.GeojsonField()
    # spacial_resolution = # Create Spatial Resolution Field
    # temporal_extent = # Create Temporal Extent Field
    # categories = # Create Class
    # color_scheme = # Create Color Scheme
    # metadata = # Create Metadata class
    # permissions = (READ, WRITE, UPDATE, DELETE)
    # protocols =  (WebSocket, WebHook, WebRTC)
