###############################################################################
# Filename: test_MapsetInfoResponseModelSerializer.py                          #
# Project: OpenPlains Inc.                                                     #
# File Created: Sunday December 17th 2023                                      #
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

from django.test import TestCase
from grass.serializers import MapsetInfoResponseSerializer


class MapsetInfoResponseModelSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            "status": "success",
            "user_id": "123",
            "resource_id": "456",
            "message": "Data processed successfully",
            "accept_timestamp": 1234567890.0,
            "accept_datetime": "2022-01-01 12:00:00",
            "timestamp": 1234567890.0,
            "datetime": "2022-01-01 12:00:00",
        }
        serialized_data = MapsetInfoResponseSerializer(data=data)
        self.assertTrue(serialized_data.is_valid())

    def test_invalid_data(self):
        data = {
            "status": "success",
            "user_id": "123",
            "resource_id": "456",
            "message": "Data processed successfully",
            "accept_timestamp": "invalid",
            "accept_datetime": "2022-01-01 12:00:00",
            "timestamp": 1234567890.0,
            "datetime": "2022-01-01 12:00:00",
        }
        serialized_data = MapsetInfoResponseSerializer(data=data)
        self.assertFalse(serialized_data.is_valid())

    def test_optional_fields(self):
        data = {
            "status": "success",
            "user_id": "123",
            "resource_id": "456",
            "message": "Data processed successfully",
            "accept_timestamp": 1234567890.0,
            "accept_datetime": "2022-01-01 12:00:00",
            "timestamp": 1234567890.0,
            "datetime": "2022-01-01 12:00:00",
            "queue": "default",
            "process_log": [],
            "process_chain_list": [],
            "process_results": {
                "projection": "4326",
                "region": {
                    "w": 0.0,
                    "s": 0.0,
                    "e": 10.0,
                    "n": 10.0,
                },
            },
            "progress": {
                "step": 1,
                "num_of_steps": 10,
                "sub_step": 2,
                "num_sub_steps": 10,
            },
            "exception": {
                "message": "Test message",
                "type": "Test type",
                "traceback": ["Line 1", "Line 2", "Line 3"],
            },
            "time_delta": 10.0,
            "http_code": 200.0,
            "urls": {"status": "OK", "resources": ["https://path.com"]},
            "api_info": {
                "endpoint": "https://path.com",
                "method": "GET",
                "path": "/path",
                "request_url": "https://path.com/path",
                "post_url": "https://path.com/path",
            },
        }
        serialized_data = MapsetInfoResponseSerializer(data=data)
        self.assertTrue(serialized_data.is_valid())

    def test_missing_required_fields(self):
        data = {
            "status": "success",
            "user_id": "123",
            "message": "Data processed successfully",
            "accept_timestamp": 1234567890.0,
            "accept_datetime": "2022-01-01 12:00:00",
            "timestamp": 1234567890.0,
            "datetime": "2022-01-01 12:00:00",
        }
        serialized_data = MapsetInfoResponseSerializer(data=data)
        self.assertFalse(serialized_data.is_valid())
