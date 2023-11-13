###############################################################################
# Filename: test_Token.py                                                      #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday November 10th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Nov 13 2023                                               #
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


from django.test import TestCase
from django.utils import timezone
from grass.models import Token
from django.contrib.auth.models import User
from grass.models import ActiniaUser
from grass.models.enums import TokenTypeEnum


class TokenModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )

        cls.actinia_user = ActiniaUser.objects.create(
            actinia_username="testuser",
            actinia_role="admin",
            user=cls.user,
            password="testpass",
        ).save()

    def test_is_expired_with_future_date(self):
        """
        is_expired() should return False for a token with a future expiration date
        """
        future_date = timezone.now() + timezone.timedelta(days=1)
        token = Token.objects.create(
            token="testtoken",
            user=self.user,
            actinia_user=self.actinia_user,
            expires=future_date,
            token_type=TokenTypeEnum.USER,
        )
        self.assertFalse(token.is_expired())

    def test_is_expired_with_past_date(self):
        """
        is_expired() should return True for a token with a past expiration date
        """
        past_date = timezone.now() - timezone.timedelta(days=1)
        token = Token.objects.create(
            token="testtoken",
            user=self.user,
            actinia_user=self.actinia_user,
            expires=past_date,
            token_type=TokenTypeEnum.USER,
        )
        self.assertTrue(token.is_expired())

    def test_is_active_with_future_date(self):
        """
        is_active() should return True for a token with a future expiration date
        """
        future_date = timezone.now() + timezone.timedelta(days=1)
        token = Token.objects.create(
            token="testtoken",
            user=self.user,
            actinia_user=self.actinia_user,
            expires=future_date,
            token_type=TokenTypeEnum.USER,
        )
        self.assertTrue(token.is_active())

    def test_is_active_with_past_date(self):
        """
        is_active() should return False for a token with a past expiration date
        """
        past_date = timezone.now() - timezone.timedelta(days=1)
        token = Token.objects.create(
            token="testtoken",
            user=self.user,
            actinia_user=self.actinia_user,
            expires=past_date,
            token_type=TokenTypeEnum.USER,
        )
        self.assertFalse(token.is_active())
