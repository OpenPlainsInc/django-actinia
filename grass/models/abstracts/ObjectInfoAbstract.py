###############################################################################
# Filename: ObjectInfoAbstract.py                                              #
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

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.crypto import get_random_string
import uuid


class ObjectInfoAbstract(models.Model):
    """
    Abstract class to add basic details to a database object
    """

    # TODO: Create PR to update model ids to uuids
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=250, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=True, on_delete=models.CASCADE
    )
    public = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, blank=True, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.name)
            unique_slug = original_slug
            num = 1
            while self.__class__.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{original_slug}-{get_random_string(4)}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
