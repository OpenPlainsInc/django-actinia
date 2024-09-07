###############################################################################
# Filename: baseUser.py                                                        #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday September 6th 2024                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Fri Sep 06 2024                                               #
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
from django.contrib.auth.models import User
from grass.models import ActiniaUser
from django.db import transaction
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def actinia_user_created(sender, instance, created, **kwargs):
    try:
        # actinia_user_service = ActiniaUserService()
        if created:
            # The code here will run after a Location instance is created
            logger.info(f"User {instance.username} was created.")
            logger.info(f"Attempting to create ActiniaUser for {instance.username}.")

            # This will trigger another sigle to handle creating the actinia user.
            try:
                actinia_user = ActiniaUser.objects.create(
                    user=instance,
                    actinia_username=instance.username,
                )
                logger.info(f"ActiniaUser Model created: {actinia_user}.")
            except Exception as e:
                logger.error(
                    f"Failed to create ActiniaUser for User {instance.username}: {str(e)}",
                    exc_info=True,
                )
                notify_admin(instance)

            # Sync the new ActiniaUser with the third-party API

        else:
            # Perform actions specific to updates to an existing ActiniaUser
            logger.info(f"Failed to create User: {instance.actinia_username}")

    except Exception as e:
        logger.error(f"Error during post_save for ActiniaUser: {str(e)}", exc_info=True)


@receiver(pre_delete, sender=User)
def actinia_user_deleted(sender, instance, **kwargs):
    # The code here will run before a Location instance is deleted
    if instance.actinia_user is None:
        logger.warning(f"User {instance.username} does not have an ActiniaUser.")
        return None

    print(f"ActiniaUser {instance.actinia_user.id} is about to be deleted.")
    try:
        with transaction.atomic():
            instance.actinia_user.delete()
            logger.info(f"ActiniaUser {instance.actinia_username} was deleted.")
    except Exception as e:
        logger.error(f"Failed to delete ActiniaUser: {str(e)}", exc_info=True)
        raise ValidationError(f"Failed to delete ActiniaUser: {str(e)}")


def notify_admin(instance):
    # Example function to notify an admin about the new user
    # This could be an email, a Slack message, or another form of notification
    logger.info(
        f"Notifying admin about new ActiniaUser attached to User: {instance.actinia_user}"
    )
