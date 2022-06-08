###############################################################################
# Filename: utils.py                                                           #
# Project: OpenPlains                                                          #
# File Created: Monday June 6th 2022                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Jun 06 2022                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2022 OpenPlains                                                #
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

from django.conf import settings
from requests.auth import HTTPBasicAuth
import json
import os
from django.contrib.gis.gdal import DataSource
import time
import requests
from functools import reduce

# from channels.layers import get_channel_layer
# from actinia import Actinia


import re

# import simplejson # should we load
import sys

# import grass.script as grass # should we load
import subprocess

# from pprint import pprint
from typing import List, Optional

ACTINIA_SETTINGS = settings.ACTINIA


# actinia_con = Actinia(os.path.join('http://', ACTINIA_SETTINGS['ACTINIA_BASEURL']), ACTINIA_SETTINGS['ACTINIA_VERSION'])
# print(actinia_con.get_version())
# actinia_con.set_authentication(ACTINIA_SETTINGS['ACTINIA_USER'], ACTINIA_SETTINGS['ACTINIA_PASSWORD'])


def currentUser():
    return ACTINIA_SETTINGS["ACTINIA_USER"]


# def authorizeUser():
#     actinia_con.set_authentication(ACTINIA_SETTINGS['ACTINIA_USER'], ACTINIA_SETTINGS['ACTINIA_PASSWORD'])
#     return actinia_con


def print_as_json(data):
    return json.dumps(data)


def auth():
    # print(ACTINIA_SETTINGS)
    auth = HTTPBasicAuth(
        ACTINIA_SETTINGS["ACTINIA_USER"], ACTINIA_SETTINGS["ACTINIA_PASSWORD"]
    )
    return auth


def baseUrl():
    ACTINIA_URL = os.path.join(
        "http://",
        ACTINIA_SETTINGS["ACTINIA_BASEURL"],
        "api",
        ACTINIA_SETTINGS["ACTINIA_VERSION"],
    )
    # print(ACTINIA_URL)
    return ACTINIA_URL


# def locations():
#     locations = actinia_con.get_locations()
#     return locations


# def locationInfo(locations, location):
#     info = locations[location].get_info()
#     return info


def location():
    return ACTINIA_SETTINGS["ACTINIA_LOCATION"]


# def mapsets(location):
#     mapsets = location.get_mapsets()
#     print(mapsets.keys())
#     return mapsets


def resourceStatus(user_id, resource_id):
    url = f"{baseUrl()}/resources/{user_id}/{resource_id}"
    r = requests.get(url, auth=auth())
    data = r.json()
    print(f"resourceStatus: {r.status_code}")
    if r.status_code == 200:
        if data["status"] == "finished":
            print(f"Finished Resource: {data}")
            return data["urls"]["resources"]
        else:
            return resourceStatus(user_id, resource_id)


def split_grass_command(grass_command: str):
    """Split grass command at spaces exluding spaces in quotes. Additional for
    e.g. r.mapcalc the quotes are removed from the GRASS option value if the
    value starts and ends with quotes
    Args:
        grass_command: A string of a GRASS GIS command
    Returns:
        The splitted GRASS GIS command needed for create_actinia_process
    """
    SPACE_MATCHER = re.compile(r" (?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
    EQUALS_MATCHER = re.compile(r"=(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")

    tokens = SPACE_MATCHER.split(grass_command)
    for i, token in enumerate(tokens):
        if "=" in token and ("'" in token or '"' in token):
            par, val = EQUALS_MATCHER.split(token)
            if val.startswith(val[-1]):
                tokens[i] = "%s=%s" % (par, val.strip('"').strip("'"))
    return tokens


def create_actinia_process_chain(command: List[dict]) -> Optional[dict]:

    PCHAIN = {"version": "1", "list": list()}
    PCHAIN.update({"list": command})

    return PCHAIN


def create_actinia_process(command: List[str]) -> Optional[dict]:
    """Create an actinia command dict, that can be put into a process chain
    Args:
        command: The GRASS GIS command as a list of strings
    Returns:
        The actinia process dictionary
    """

    if not command:
        return None

    print(command)

    # This should all be saved to a users request record
    # cmd = {
    #     "id": None,  # UserID and Timestamp or requestId
    #     "module": None,
    #     "inputs": []
    # }

    cmd = dict(id=command[0], module=command[0], inputs=list(), flags="")

    inputs = command[1:]

    # Get Flags
    flags = "".join(list(filter(lambda x: x.startswith("-"), inputs))).replace("-", "")
    print(f"Params List: {flags}")
    cmd.update({"flags": flags})
    # Get Params
    param_list = list(filter(lambda x: "=" in x, inputs))
    print(f"Params List: {param_list}")
    input_dict = []
    for x in param_list:
        print(x.split("="))
        param, value = x.split("=")
        input_dict.append(dict(param=param, value=value))

    cmd.update({"inputs": input_dict})

    print(cmd)
    return cmd


def is_grass_command(grass_command: str):
    """Check if the given command is a GRASS GIS command
    Args:
        grass_command: A string of a GRASS GIS command
    Returns:
        True if the command is a GRASS GIS command otherwise False
    """
    if grass_command.split(".")[0] in ["r", "v", "i", "t", "g", "r3"]:
        return True
    else:
        return False
