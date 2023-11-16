###############################################################################
# Filename: ingest.py                                                          #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday November 13th 2023                                      #
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

import requests
from django.conf import settings

ACTINIA_SETTINGS = settings.ACTINIA


class Ingest:
    def __init__(self):
        self.ingest_url = ACTINIA_SETTINGS["ACTINIA_SWAGGER_URL"]
        self.model_definitions = {}
        self.path_definitions = {}

    def create_models(self, model_definitions):
        pass

    def create_views(self, paths):
        for path in paths:
            for method in paths[path]:
                print("Ingesting {} {}".format(method, path))

    def create_routes(self, path_definitions):
        pass

    def ingest_api(self):
        r = requests.get(self.ingest_url)
        if r.status_code == 200:
            swagger = r.json()
            self.path_definitions = swagger["paths"]
            self.model_definitions = swagger["definitions"]
            self.create_models(self.model_definitions)
            self.create_views(self.path_definitions)
            self.create_routes(self.path_definitions)
        else:
            raise Exception("Could not ingest api from {}".format(self.ingest_url))


def __main__():
    ingest = Ingest()
    ingest.ingest_api()
