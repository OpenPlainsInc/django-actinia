###############################################################################
# Filename: test_locations.py                                                  #
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

from django.test import TestCase
from grass.models import Location, ActiniaUser
from django.contrib.auth.models import User
from grass.models.enums import RolesEnum


class SignalTests(TestCase):
    def test_location_created_signal(self):
        # Create a User instance
        user = User.objects.create(username="testuser55", password="testpass")

        # Create an ActiniaUser instance
        actinia_user = ActiniaUser.objects.create_actinia_user(
            user=user, actinia_role=RolesEnum.ADMIN.value
        )

        # Create a Location instance
        location = Location.objects.create(
            owner=user,
            name="testlocation3358",
            description="testlocation3358",
            epsg=3358,
        )

        location.actinia_users.set([actinia_user])

        location.save()

        # At this point, your location_created signal should have been sent.
        # You can now check that the expected outcome occurred.
        # This will depend on what your signal does.
        # For example, if your signal creates a new Mapset instance, you could do:
        # self.assertTrue(Mapset.objects.filter(location=location).exists())

        self.assertTrue(Location.objects.filter(name="testlocation3358").exists())
