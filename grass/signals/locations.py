###############################################################################
# Filename: locations.py                                                       #
# Project: OpenPlains Inc.                                                     #
# File Created: Thursday March 7th 2024                                        #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Mar 08 2024                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2024 OpenPlains Inc.                                           #
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

from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from grass.models import Location
from grass.services import ProjectService
from django.core.exceptions import ValidationError


@receiver(pre_save, sender=Location)
def location_pre_save_created(sender, instance, **kwargs):
    try:
        project_service = ProjectService()
        project_service.create_project(
            project_name=instance.name, project_epsg=instance.epsg
        )
    except Exception as e:
        raise ValidationError(f"Failed to create location: {str(e)}")


@receiver(post_save, sender=Location)
def location_created(sender, instance, created, **kwargs):
    if created:
        # The code here will run after a Location instance is created
        print(f"Location {instance.name} was created.")


@receiver(pre_delete, sender=Location)
def location_deleted(sender, instance, **kwargs):
    # The code here will run before a Location instance is deleted
    print(f"Location {instance.name} is about to be deleted.")
    try:
        project_service = ProjectService()
        project_service.delete_project(project_name=instance.name)
    except Exception as e:
        raise ValidationError(f"Failed to delete location: {str(e)}")
