###############################################################################
# Filename: Mapset.py                                                          #
# Project: django-actinia                                                      #
# File Created: Tuesday June 7th 2022                                          #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Jun 07 2022                                               #
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
from actinia.models.ObjectInfoAbstract import ObjectInfoAbstract
from actinia.models.Location import Location


class Mapset(ObjectInfoAbstract):
    """
    Class representing GRASS mapsets avaliable in Actinia

    Attributes
    ----------
    id : BigAutoField
        Auto generated Primary key of response
    name : str
        The name of the GRASS mapset
    description: str
        The EPSG code of the location
    owner : User
        The user who owns the mapset
    teams : Team
        The teams that have access to the mapset.
    location : Location
        The 'Location' instance the mapset belongs to.
    """

    location = models.ForeignKey(
        Location, editable=False, on_delete=models.CASCADE, related_name="mapsets"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "location", "owner"], name="unique_mapset"
            )
        ]

    def layers_count():
        """
        Returns the number of layers in the mapset
        """
        pass

    def layers(datatype=None):
        """
        Returns the layers in the mapset
        """
        pass
