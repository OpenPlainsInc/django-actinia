###############################################################################
# Filename: actiniaUser.py                                                     #
# Project: OpenPlains Inc.                                                     #
# File Created: Thursday March 21st 2024                                       #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Sep 03 2024                                               #
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
from grass.models import ActiniaUser
from grass.services import ActiniaUserService
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=ActiniaUser)
def actinia_user_pre_save_created(sender, instance, **kwargs):
    try:
        actinia_user_service = ActiniaUserService()

        # Use a custom name if it is set otherwise use the username of the user
        actinia_username = (
            instance.actinia_username
            if instance.actinia_username
            else instance.user.username
        )
        actinia_role = (
            instance.get_actinia_role_display()
        )  # get the label of actinia_role

        # Generate a password if none is provided
        if not instance.password:
            password = get_random_string(23)
            instance.password = password  # Save the generated password to the instance
        else:
            password = instance.password

        actinia_user_service.create_actinia_user(
            user=actinia_username,
            group=actinia_role,
            user_id=actinia_username,
            password=password,
        )
    except Exception as e:
        logger.error(f"Failed to create ActiniaUser: {str(e)}", exc_info=True)
        raise ValidationError(f"Failed to create ActiniaUser: {str(e)}")


@receiver(post_save, sender=ActiniaUser)
def actinia_user_created(sender, instance, created, **kwargs):
    try:
        # actinia_user_service = ActiniaUserService()
        if created:
            # The code here will run after a Location instance is created
            logger.info(f"ActiniaUser {instance.actinia_username} was created.")

            # Add extra notifications or actions for new ActiniaUser instances
            notify_admin(instance)

            # Sync the new ActiniaUser with the third-party API

        else:
            # Perform actions specific to updates to an existing ActiniaUser
            logger.info(
                f"ActiniaUser updated (Not Implemented): {instance.actinia_username}"
            )
            # Example: Sync updated details with the third-party API
            # actinia_user_service.update_actinia_user(
            #     user=instance.actinia_username,
            #     group=instance.get_actinia_role_display(),
            #     user_id=instance.actinia_username,
            #     password=instance.password,
            # )
    except Exception as e:
        logger.error(f"Error during post_save for ActiniaUser: {str(e)}", exc_info=True)


@receiver(pre_delete, sender=ActiniaUser)
def actinia_user_deleted(sender, instance, **kwargs):
    # The code here will run before a Location instance is deleted
    print(f"ActiniaUser {instance.actinia_username} is about to be deleted.")
    try:
        actinia_user_service = ActiniaUserService()
        actinia_user_service.delete_actinia_user(
            actinia_username=instance.actinia_username
        )
    except Exception as e:
        logger.error(f"Failed to delete ActiniaUser: {str(e)}", exc_info=True)
        raise ValidationError(f"Failed to delete ActiniaUser: {str(e)}")


def notify_admin(instance):
    # Example function to notify an admin about the new user
    # This could be an email, a Slack message, or another form of notification
    logger.info(f"Notifying admin about new ActiniaUser: {instance.actinia_username}")
