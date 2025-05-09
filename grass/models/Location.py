###############################################################################
# Filename: Location.py                                                        #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday June 7th 2022                                          #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Sep 06 2024                                               #
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

from .abstracts.ObjectAuditAbstract import ObjectAuditAbstract
from .abstracts.ObjectInfoAbstract import ObjectInfoAbstract
from django.db import models
from grass.validators import validate_no_spaces


class Location(ObjectAuditAbstract, ObjectInfoAbstract):
    """
    Class representing GRASS locations avaliable in Actinia

    Attributes
    ----------
    id : BigAutoField
        Auto generated Primary key of response
    name : str
        The name of the GRASS location
    description: str
        The EPSG code of the location
    owner : User
        The user who owns the location
    epsg : str
        The EPSG code of the location
    public : bool
        Set true if location is publicly avaliable to all users.
    slug : str
    """

    name = models.CharField(
        max_length=255, blank=False, validators=[validate_no_spaces]
    )
    epsg = models.CharField(max_length=8, blank=False)
    actinia_users = models.ManyToManyField("ActiniaUser", related_name="projects")

    def save(self, *args, **kwargs):
        """
        Create a new location.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "epsg", "owner")
        ordering = ["-updated_on"]
