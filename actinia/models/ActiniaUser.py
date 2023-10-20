###############################################################################
# Filename: ActiniaUser.py                                                     #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday June 6th 2022                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Oct 20 2023                                               #
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

from django.db import models
from django.contrib.auth.models import BaseUserManager
from .ObjectAuditAbstract import ObjectAuditAbstract
from .fields.ActiniaRoleEnumField import ActiniaRoleEnumField


class ActiniaUser(ObjectAuditAbstract):
    """
    Custom user class to manage actinia user.

    Attributes:
        actinia_username (str): The username of the actinia user.
        actinia_role (ActiniaRoleEnumField): The role of the actinia user.
        user (ForeignKey): The related Django user object.
        password (str): The password of the actinia user.
    """

    actinia_username = models.CharField(max_length=50, blank=False, unique=True)
    actinia_role = ActiniaRoleEnumField()
    user = models.ForeignKey(
        "auth.User", related_name="actinia_users", on_delete=models.CASCADE
    )
    password = models.CharField(max_length=128)
    # password = # https://docs.djangoproject.com/en/4.0/topics/auth/passwords/#scrypt-usage

    def _generateActiniaPassword(self):
        """
        Generate a password for managed actinia user.
        """
        new_password = BaseUserManager.make_random_password()
        self.password = new_password

    def generateActiniaToken(self):
        """
        Generate authorization token for user and store in Tokens
        """
        pass

    def refreshActiniaToken(self):
        """
        Refresh users authentication token
        """
        pass

    def locations(self):
        """
        Get a list of user's locations
        """
        pass

    def teams(self):
        """
        Get a list of user's teams
        """
        pass

    def projects(self):
        """
        Get a list of user's projects
        """
        pass

    def grass_templates(self):
        """
        Get list of user's GRASS Templates
        """
        pass

    def save(self, *args, **kwargs):
        """
        Create a new actinia user.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Create a new Actinia user account

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
