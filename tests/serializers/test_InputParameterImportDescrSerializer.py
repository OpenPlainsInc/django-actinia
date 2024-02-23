###############################################################################
# Filename: test_InputParameterImportDescrSerializer.py                        #
# Project: OpenPlains Inc.                                                     #
# File Created: Sunday December 17th 2023                                      #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Sun Dec 17 2023                                               #
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


import pytest
from grass.serializers.InputParameterImportDescrSerializer import (
    InputParameterImportDescrSerializer,
)


@pytest.mark.parametrize(
    "data",
    [
        {
            "type": "raster",
            "source": "http://example.com/raster.tif",
            "resample": "bilinear",
            "resolution": "estimated",
        },
        {
            "type": "vector",
            "source": "http://example.com/vector.shp",
            "extent": "10,20,30,40",
            "filter": "attribute='value'",
        },
        {
            "type": "landsat",
            "source": "LT52170762005240COA00",
            "landsat_atcor": "dos1",
            "semantic_label": "red",
        },
    ],
)
def test_InputParameterImportDescrSerializer(data):
    serializer = InputParameterImportDescrSerializer(data=data)
    assert serializer.is_valid()
