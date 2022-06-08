###############################################################################
# Filename: ActiniaUser.py                                                     #
# Project: OpenPlains                                                          #
# File Created: Monday June 6th 2022                                           #
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
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User
from actinia.models.ObjectAuditAbstract import ObjectAuditAbstract
from actinia.models.fields import ActiniaRoleEnumField


class ActiniaUser(ObjectAuditAbstract):
    """
    Custom user class to manage actinia user.
    """

    actinia_username = models.CharField(max_length=50, blank=False, unique=True)
    actinia_role = ActiniaRoleEnumField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    # password = # https://docs.djangoproject.com/en/4.0/topics/auth/passwords/#scrypt-usage

    def generateActiniaPassword(self):
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
