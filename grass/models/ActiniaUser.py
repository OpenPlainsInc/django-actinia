###############################################################################
# Filename: ActiniaUser.py                                                     #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday June 6th 2022                                           #
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
# the Free Software Foundation, .either version 3 of the License, or           #
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

# import os
from typing import Any
from django.db import models
from django.utils.crypto import get_random_string
from .abstracts.ObjectAuditAbstract import ObjectAuditAbstract
from .fields.ActiniaRoleEnumField import ActiniaRoleEnumField
from django.conf import settings


class ActiniaUser(ObjectAuditAbstract):
    """
    Custom user class to manage actinia user.

    Attributes:
        actinia_username (str): The username of the actinia user.
        actinia_role (ActiniaRoleEnumField): The role of the actinia user.
        user (ForeignKey): The related Django user object.
        password (str): The password of the actinia user.
    """

    id = models.BigAutoField(primary_key=True, editable=False)
    actinia_username = models.CharField(max_length=50, blank=False, unique=True)
    actinia_role = ActiniaRoleEnumField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="actinia_user", on_delete=models.CASCADE
    )
    password = models.CharField(max_length=128, blank=True)
    api_token = models.CharField(
        max_length=255, blank=True
    )  # Token for third-party API access

    def save(self, *args, **kwargs):
        # Trigger the pre_save and post_save signal
        """
        Save an actinia user. This could mean creating a new user or updating an existing one.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Triggers the pre_delete signal
        super().delete(*args, **kwargs)

    def __str__(self):
        """
        Return the actinia username.

        Returns:
            str: The actinia username.
        """
        return self.actinia_username

    class Meta:
        """
        Metadata for the ActiniaUser model.
        """

        ordering = ["created_on"]
        verbose_name = "Actinia User"
        verbose_name_plural = "Actinia Users"
        db_table = "actinia_users"
