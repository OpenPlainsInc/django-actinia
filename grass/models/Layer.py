###############################################################################
# Filename: Layer.py                                                           #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday November 27th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Sep 03 2024                                               #
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
from .abstracts.ObjectAuditAbstract import ObjectAuditAbstract
from .abstracts.ObjectInfoAbstract import ObjectInfoAbstract
from .Mapset import Mapset
from .ActiniaUser import ActiniaUser
from .fields import LayerTypeEnumField
from django.contrib.gis.db import models as gis_models


class Layer(ObjectAuditAbstract, ObjectInfoAbstract):
    """
    GRASS Layer class
    """

    mutable = models.BooleanField(default=False)
    mapset = models.ForeignKey(Mapset, related_name="layers", on_delete=models.CASCADE)
    actinia_owner = models.ManyToManyField(ActiniaUser, related_name="layers")
    layer_type = LayerTypeEnumField()
    size = models.CharField()  # KB
    eres = models.FloatField()
    wres = models.FloatField()
    stac_asset = models.URLField()
    thumbnail = models.URLField()
    bbox = gis_models.PolygonField()
    # spacial_resolution = # Create Spatial Resolution Field
    # temporal_extent = # Create Temporal Extent Field
    # categories = # Create Class
    # color_scheme = # Create Color Scheme
    # metadata = # Create Metadata class
    # protocols =  (WebSocket, WebHook, WebRTC)

    def has_permission(self, user, action, context=None):
        return self.mapset.has_permission(user, action, context)

    def __str__(self):
        return f"{self.name} ({self.layer_type})"
