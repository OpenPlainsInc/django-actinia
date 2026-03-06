###############################################################################
# Filename: LocationDetailSerializer.py                                        #
# Project: OpenPlains Inc.                                                     #
# File Created: Friday February 2025                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2025 OpenPlains Inc.                                           #
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

import re
from rest_framework import serializers
from .LocationSerializer import LocationSerializer


def extract_bbox_from_wkt(wkt):
    """
    Extract BBOX values from a WKT projection string.

    Parameters
    ----------
    wkt : str
        A WKT projection string.

    Returns
    -------
    list[float] or None
        A list of four floats [lat_min, lon_min, lat_max, lon_max], or None
        if the BBOX could not be parsed.
    """
    if not wkt:
        return None
    match = re.search(r"BBOX\[([^\]]+)\]", wkt)
    if match:
        try:
            return [float(v.strip()) for v in match.group(1).split(",")]
        except (ValueError, AttributeError):
            return None
    return None


def extract_unit_from_wkt(wkt):
    """
    Extract the linear or angular unit from a WKT projection string.

    Parameters
    ----------
    wkt : str
        A WKT projection string.

    Returns
    -------
    str or None
        A human-readable unit string (e.g. "meters", "feet", "degrees"),
        or None if the unit could not be determined.
    """
    if not wkt:
        return None
    match = re.search(r'LENGTHUNIT\["([^"]+)"', wkt)
    if match:
        unit_name = match.group(1).lower()
        if "metre" in unit_name or "meter" in unit_name:
            return "meters"
        if "foot" in unit_name or "feet" in unit_name:
            return "feet"
        return unit_name
    if re.search(r"ANGLEUNIT\[", wkt):
        return "degrees"
    return None


class LocationDetailSerializer(LocationSerializer):
    """
    Serializer for the detailed location response.

    Extends :class:`LocationSerializer` with additional read-only fields
    sourced from the Actinia ``GET /locations/{location_name}/info`` endpoint:

    Attributes
    ----------
    region : dict, optional
        The current computational region of the location.
    bbox : list[float], optional
        The bounding box of the location CRS as
        ``[lat_min, lon_min, lat_max, lon_max]``.
    unit : str, optional
        The linear or angular unit of the location CRS (e.g. "meters").
    mapsets : list[str], optional
        The names of mapsets that belong to this location.
    """

    region = serializers.DictField(required=False, read_only=True, allow_null=True)
    bbox = serializers.ListField(
        child=serializers.FloatField(), required=False, read_only=True, allow_null=True
    )
    unit = serializers.CharField(required=False, read_only=True, allow_null=True)
    mapsets = serializers.ListField(child=serializers.CharField(), required=False, read_only=True)

    class Meta(LocationSerializer.Meta):
        fields = LocationSerializer.Meta.fields + ["region", "bbox", "unit", "mapsets"]
        read_only_fields = LocationSerializer.Meta.read_only_fields + [
            "region",
            "bbox",
            "unit",
            "mapsets",
        ]
