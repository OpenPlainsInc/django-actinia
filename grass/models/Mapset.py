###############################################################################
# Filename: Mapset.py                                                          #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday June 7th 2022                                          #
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
from django.core.exceptions import ValidationError
from .Location import Location
from .Permission import Permission
from .abstracts.ObjectInfoAbstract import ObjectInfoAbstract
from .abstracts.ObjectAuditAbstract import ObjectAuditAbstract
from django.contrib.contenttypes.models import ContentType


class Mapset(ObjectInfoAbstract, ObjectAuditAbstract):
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
    location : Location
        The 'Location' instance the mapset belongs to.
    users : models.ManyToManyField
        The users who have access to the mapset.
    """

    project = models.ForeignKey(
        Location, editable=False, on_delete=models.CASCADE, related_name="mapsets"
    )
    allowed_users = models.ManyToManyField(
        "ActiniaUser", related_name="accessible_mapsets"
    )

    class Meta:
        unique_together = (
            "name",
            "project",
            "owner",
        )  # This enforces uniqueness across these three fields within the Mapset model.

        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["name", "location", "owner"], name="unique_mapset"
        #     )
        # ]\

    def clean(self):
        # Custom validation to check for unique combination across models
        if Mapset.objects.filter(
            name=self.name, location__name=self.location.name, owner=self.owner
        ).exists():
            raise ValidationError(
                "A mapset with this name, location, and owner already exists."
            )

    def save(self, *args, **kwargs):
        self.clean()  # Perform custom validation
        super(Mapset, self).save(*args, **kwargs)

    def has_permission(self, user, action, context=None):
        # Check if the user has direct permission or belongs to the allowed users
        if self.owner == user or self.allowed_users.filter(id=user.id).exists():
            return True

        # Check specific permissions
        permissions = Permission.objects.filter(
            actinia_user=user,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            action=action,
        )
        return any(perm.is_valid(context=context) for perm in permissions)

    def __str__(self):
        return f"{self.location.name} - {self.name}"
