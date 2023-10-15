###############################################################################
# Filename: tasks.py                                                           #
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
# Copyright (c) 2023 OpenPlains                                                #
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

from celery import shared_task
import actinia.utils as acp

# from actinia import *
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task()
def asyncResourceStatus(user_id, resource_id):
    """
    Poll actinia api to check on status of process chain resource.

    Parameters
    ----------
    user_id : string
        The requesting user's id
    resource_id: string
        The id of the actinia resource.

    Returns:
        Any: _description_
    """

    # Make request to actinia to check resource status
    url = f"{acp.baseUrl()}/resources/{user_id}/{resource_id}"
    r = requests.get(url, auth=acp.auth())
    data = r.json()
    if r.status_code == 200:
        channel_layer = get_channel_layer()
        resource_name = resource_id.replace("-", "_")
        updated_status = data["status"]
        resources = data["urls"]["resources"]
        process_log = []
        if data.get("process_log") is not None:
            process_log = data["process_log"]

        resource_group = f"actinia_{resource_name}"

        # Response with message back to to consumer
        response_message = {
            "type": "resource_message",
            "message": updated_status,
            "resource_id": resource_id,
            "resources": resources,
            "process_log": process_log,
        }

        return async_to_sync(channel_layer.group_send)(resource_group, response_message)


#
