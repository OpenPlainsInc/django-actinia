###############################################################################
# Filename: ActiniaUser.py                                                     #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday November 14th 2023                                     #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Nov 14 2023                                               #
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ActiniaUserService import ActiniaUserService, USER_TASK


class ActiniaUserView(APIView):
    def get(self, request, task, format=None):
        service = ActiniaUserService()
        task = USER_TASK(task)

        if task == USER_TASK.USERS:
            # Call the method to get users
            data = service.get_users()
        elif task == USER_TASK.TOKEN:
            # Call the method to get token
            data = service.get_token()
        elif task == USER_TASK.API_KEY:
            # Call the method to get API key
            data = service.get_api_key()
        elif task == USER_TASK.API_LOG:
            # Call the method to get API log
            data = service.get_api_log()
        else:
            return Response(
                {"error": "Invalid task"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(data)
