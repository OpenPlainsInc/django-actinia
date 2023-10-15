###############################################################################
# Filename: Location.py                                                        #
# Project: OpenPlains                                                          #
# File Created: Tuesday June 7th 2022                                          #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Jun 07 2022                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2022 OpenPlains                                                #
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
from actinia.models.ObjectAuditAbstract import ObjectAuditAbstract
from actinia.models.ActiniaUser import ActiniaUser


class Location(ObjectAuditAbstract):
    """
    Class representing GRASS locations avaliable in Actinia

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
    epsg : str
        The EPSG code of the location
    organization : Organization
        The organization the location belongs to
    teams : Team
        The teams that have access to the location
    public : bool
        Set true if location is publicly avaliable to all users.
    """

    epsg = models.CharField(max_length=8, blank=False)

    # def mapsets(self):
    #     """Return mapsets for this location"""
    #     return Mapset.objects.get(location=self)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["location_name", "epsg", "owner", "team", "organization"],
                name="unique_location",
            )
        ]
