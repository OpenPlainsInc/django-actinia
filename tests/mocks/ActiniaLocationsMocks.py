###############################################################################
# Filename: ActiniaLocationsMocks.py                                           #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday March 25th 2024                                         #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Mar 25 2024                                               #
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


class ActiniaLocationsAPIMocks:

    # Actinia Location Requests
    @staticmethod
    def get_locations(location_list=["nc_spm_08"]):
        """Mock response for a getting locations GET: /locations"""
        return {"locations": ["nc_spm_08", "test_location"], "status": "success"}

    @staticmethod
    def get_location_info(location_id):
        """Mock response for deleting a user at GET: /locations/:location_name/info"""
        pass

    @staticmethod
    def get_location_info_error(location_id):
        """Mock error response for deleting a user at GET: /locations/:location_name/info"""
        pass

    @staticmethod
    def create_location(location_id, epsg):
        """Mock response for deleting a user at POST: /locations/:location_name"""
        pass

    @staticmethod
    def create_location_error(location_id, epsg):
        """Mock error response for deleting a user at POST: /locations/:location_name"""
        pass

    @staticmethod
    def delete_location(location_id):
        """Mock response for deleting a user at DELETE: /locations/:location_name"""
        pass

    @staticmethod
    def delete_location_error(location_id):
        """Mock error response for deleting a user at DELETE: /locations/:location_name"""
        pass
