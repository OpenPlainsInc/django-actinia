###############################################################################
# Filename: SimpleResponseModel.py                                             #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday June 6th 2022                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Wed Oct 18 2023                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2023 OpenPlains Inc.                                                #
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

from actinia.models.enums import ResponseStatusEnum
from .fields.ActiniaResourceStatusEnumField import ActiniaResourceStatusEnumField
from .fields.ActiniaResponseStatusEnumField import ActiniaResponseStatusEnumField


class SimpleResponseAbstract(models.Model):
    """
    Abstract model of Actinia's simple response model for resource responses.

    Attributes
    ----------
    message : str
        Message returned from Actinia during a request.
    """

    message = models.CharField(max_length=250)

    class Meta:
        abstract = True


class ResourceStatusModelAbstract(SimpleResponseAbstract):
    """
    Abstract model of Actinia's simple response model for resource responses.

    Attributes
    ----------
    status : str
        The response status from Actinia (accepted, running, terminated, error)
    """

    status = ActiniaResourceStatusEnumField()


class ResponseStatusModelAbstract(SimpleResponseAbstract):
    """
    Abstract model of Actinia's simple response model for response statuses.

    Attributes
    ----------
    status : str
        The response status from Actinia (success, error)
    """

    status = ActiniaResponseStatusEnumField()
