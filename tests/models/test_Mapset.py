###############################################################################
# Filename: test_Mapset.py                                                     #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday October 20th 2023                                       #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Wed Mar 06 2024                                               #
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

# from django.contrib.auth import get_user_model
# from django.test import TestCase, Client
# from grass.models import Mapset, Location


# class MapsetModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         User = get_user_model()
#         # Set up non-modified objects used by all test methods
#         cls.client = Client()
#         cls.user = User.objects.create_user(
#             username="test_user", password="test_password"
#         )
#         cls.client.force_login(cls.user)

#         location = Location.objects.create(
#             name="test_location",
#             description="test_description",
#             owner=cls.user,
#             epsg="3358",
#             public=False,
#         )

#         Mapset.objects.create(
#             name="Test Mapset",
#             description="test_description",
#             owner=cls.user,
#             location=location,
#         )
