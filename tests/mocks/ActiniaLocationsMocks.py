###############################################################################
# Filename: ActiniaLocationsMocks.py                                           #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday March 25th 2024                                         #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Sun April 14th 2024                                           #
# Modified By: Srihitha Reddy Kaalam                                           #
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
        return {"locations": location_list, "status": "success"}

    @staticmethod
    def get_location_info(location_name):
        """Mock response for getting a location info at GET: /locations/:location_name/info"""
        return {
            "accept_datetime": "2024-04-01 11:07:58.127141",
            "accept_timestamp": 1711969678.1271381,
            "api_info": {
                "endpoint": "locationmanagementresourceuser",
                "method": "GET",
                "path": f"/api/v3/locations/{location_name}/info",
                "request_url": f"http://localhost:8088/api/v3/locations/{location_name}/info",
            },
            "datetime": "2024-04-01 11:07:58.754251",
            "http_code": 200,
            "message": "Processing successfully finished",
            "process_chain_list": [
                {
                    "1": {"flags": "ug3", "module": "g.region"},
                    "2": {"flags": "fw", "module": "g.proj"},
                }
            ],
            "process_log": [
                {
                    "executable": "g.region",
                    "id": "1",
                    "parameter": ["-ug3"],
                    "return_code": 0,
                    "run_time": 0.21491360664367676,
                    "stderr": [""],
                    "stdout": "projection=99\nzone=0\nn=1\ns=0\nw=0\ne=1\nt=1\nb=0\nnsres=1\nnsres3=1\newres=1\newres3=1\ntbres=1\nrows=1\nrows3=1\ncols=1\ncols3=1\ndepths=1\ncells=1\ncells3=1\n",
                },
                {
                    "executable": "g.proj",
                    "id": "2",
                    "parameter": ["-fw"],
                    "return_code": 0,
                    "run_time": 0.3073751926422119,
                    "stderr": [""],
                    "stdout": 'PROJCRS["NAD83(HARN) / North Carolina",BASEGEOGCRS["NAD83(HARN)",DATUM["NAD83 (High Accuracy Reference Network)",ELLIPSOID["GRS 1980",6378137,298.257222101,LENGTHUNIT["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],ID["EPSG",4152]],CONVERSION["SPCS83 North Carolina zone (meters)",METHOD["Lambert Conic Conformal (2SP)",ID["EPSG",9802]],PARAMETER["Latitude of false origin",33.75,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8821]],PARAMETER["Longitude of false origin",-79,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8822]],PARAMETER["Latitude of 1st standard parallel",36.1666666666667,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8823]],PARAMETER["Latitude of 2nd standard parallel",34.3333333333333,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8824]],PARAMETER["Easting at false origin",609601.22,LENGTHUNIT["metre",1],ID["EPSG",8826]],PARAMETER["Northing at false origin",0,LENGTHUNIT["metre",1],ID["EPSG",8827]]],CS[Cartesian,2],AXIS["easting (X)",east,ORDER[1],LENGTHUNIT["metre",1]],AXIS["northing (Y)",north,ORDER[2],LENGTHUNIT["metre",1]],USAGE[SCOPE["Engineering survey, topographic mapping."],AREA["United States (USA) - North Carolina - counties of Alamance; Alexander; Alleghany; Anson; Ashe; Avery; Beaufort; Bertie; Bladen; Brunswick; Buncombe; Burke; Cabarrus; Caldwell; Camden; Carteret; Caswell; Catawba; Chatham; Cherokee; Chowan; Clay; Cleveland; Columbus; Craven; Cumberland; Currituck; Dare; Davidson; Davie; Duplin; Durham; Edgecombe; Forsyth; Franklin; Gaston; Gates; Graham; Granville; Greene; Guilford; Halifax; Harnett; Haywood; Henderson; Hertford; Hoke; Hyde; Iredell; Jackson; Johnston; Jones; Lee; Lenoir; Lincoln; Macon; Madison; Martin; McDowell; Mecklenburg; Mitchell; Montgomery; Moore; Nash; New Hanover; Northampton; Onslow; Orange; Pamlico; Pasquotank; Pender; Perquimans; Person; Pitt; Polk; Randolph; Richmond; Robeson; Rockingham; Rowan; Rutherford; Sampson; Scotland; Stanly; Stokes; Surry; Swain; Transylvania; Tyrrell; Union; Vance; Wake; Warren; Washington; Watauga; Wayne; Wilkes; Wilson; Yadkin; Yancey."],BBOX[33.83,-84.33,36.59,-75.38]],ID["EPSG",3358]]\n',
                },
            ],
            "process_results": {
                "projection": 'PROJCRS["NAD83(HARN) / North Carolina",BASEGEOGCRS["NAD83(HARN)",DATUM["NAD83 (High Accuracy Reference Network)",ELLIPSOID["GRS 1980",6378137,298.257222101,LENGTHUNIT["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],ID["EPSG",4152]],CONVERSION["SPCS83 North Carolina zone (meters)",METHOD["Lambert Conic Conformal (2SP)",ID["EPSG",9802]],PARAMETER["Latitude of false origin",33.75,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8821]],PARAMETER["Longitude of false origin",-79,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8822]],PARAMETER["Latitude of 1st standard parallel",36.1666666666667,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8823]],PARAMETER["Latitude of 2nd standard parallel",34.3333333333333,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8824]],PARAMETER["Easting at false origin",609601.22,LENGTHUNIT["metre",1],ID["EPSG",8826]],PARAMETER["Northing at false origin",0,LENGTHUNIT["metre",1],ID["EPSG",8827]]],CS[Cartesian,2],AXIS["easting (X)",east,ORDER[1],LENGTHUNIT["metre",1]],AXIS["northing (Y)",north,ORDER[2],LENGTHUNIT["metre",1]],USAGE[SCOPE["Engineering survey, topographic mapping."],AREA["United States (USA) - North Carolina - counties of Alamance; Alexander; Alleghany; Anson; Ashe; Avery; Beaufort; Bertie; Bladen; Brunswick; Buncombe; Burke; Cabarrus; Caldwell; Camden; Carteret; Caswell; Catawba; Chatham; Cherokee; Chowan; Clay; Cleveland; Columbus; Craven; Cumberland; Currituck; Dare; Davidson; Davie; Duplin; Durham; Edgecombe; Forsyth; Franklin; Gaston; Gates; Graham; Granville; Greene; Guilford; Halifax; Harnett; Haywood; Henderson; Hertford; Hoke; Hyde; Iredell; Jackson; Johnston; Jones; Lee; Lenoir; Lincoln; Macon; Madison; Martin; McDowell; Mecklenburg; Mitchell; Montgomery; Moore; Nash; New Hanover; Northampton; Onslow; Orange; Pamlico; Pasquotank; Pender; Perquimans; Person; Pitt; Polk; Randolph; Richmond; Robeson; Rockingham; Rowan; Rutherford; Sampson; Scotland; Stanly; Stokes; Surry; Swain; Transylvania; Tyrrell; Union; Vance; Wake; Warren; Washington; Watauga; Wayne; Wilkes; Wilson; Yadkin; Yancey."],BBOX[33.83,-84.33,36.59,-75.38]],ID["EPSG",3358]]\n',
                "region": {
                    "b": 0.0,
                    "cells": 1,
                    "cells3": 1,
                    "cols": 1,
                    "cols3": 1,
                    "depths": 1,
                    "e": 1.0,
                    "ewres": 1.0,
                    "ewres3": 1.0,
                    "n": 1.0,
                    "nsres": 1.0,
                    "nsres3": 1.0,
                    "projection": 99,
                    "rows": 1,
                    "rows3": 1,
                    "s": 0.0,
                    "t": 1.0,
                    "tbres": 1.0,
                    "w": 0.0,
                    "zone": 0,
                },
            },
            "progress": {"num_of_steps": 2, "step": 2},
            "queue": "local",
            "resource_id": "resource_id-b45c452d-a3a9-446a-8889-2f1480388ec8",
            "status": "finished",
            "time_delta": 0.6276640892028809,
            "timestamp": 1711969678.7539246,
            "urls": {
                "resources": [],
                "status": "https://localhost:8088/api/v3/resources/actinia-gdi/resource_id-b45c452d-a3a9-446a-8889-2f1480388ec8",
            },
            "user_id": "actinia-gdi",
        }

    @staticmethod
    def get_location_info_error(location_name):
        """Mock error response for getting a location info at GET: /locations/:location_name/info"""
        return {
            "accept_datetime": "2024-04-01 11:45:39.121550",
            "accept_timestamp": 1711971939.1215467,
            "api_info": {
                "endpoint": "locationmanagementresourceuser",
                "method": "GET",
                "path": f"/api/v3/locations/{location_name}/info",
                "request_url": f"http://localhost:8088/api/v3/locations/{location_name}/info",
            },
            "datetime": "2024-04-01 11:45:39.483442",
            "exception": {
                "message": "AsyncProcessError:  Error while running executable <g.region>",
                "traceback": [
                    '  File "/usr/lib/python3.11/site-packages/actinia_core/processing/actinia_processing/ephemeral_processing.py", line 1951, in run\n    self._execute()\n',
                    '  File "/usr/lib/python3.11/site-packages/actinia_core/processing/actinia_processing/persistent/mapset_management.py", line 140, in _execute\n    self._execute_process_list(process_list)\n',
                    '  File "/usr/lib/python3.11/site-packages/actinia_core/processing/actinia_processing/ephemeral/persistent_processing.py", line 510, in _execute_process_list\n    self._run_module(process)\n',
                    '  File "/usr/lib/python3.11/site-packages/actinia_core/processing/actinia_processing/ephemeral_processing.py", line 1495, in _run_module\n    return self._run_executable(process, poll_time)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n',
                    '  File "/usr/lib/python3.11/site-packages/actinia_core/processing/actinia_processing/ephemeral_processing.py", line 1607, in _run_executable\n    raise AsyncProcessError(\n',
                ],
                "type": "<class 'actinia_core.core.common.exceptions.AsyncProcessError'>",
            },
            "http_code": 400,
            "message": "AsyncProcessError:  Error while running executable <g.region>",
            "process_chain_list": [
                {
                    "1": {"flags": "ug3", "module": "g.region"},
                    "2": {"flags": "fw", "module": "g.proj"},
                }
            ],
            "process_log": [
                {
                    "executable": "g.region",
                    "id": "1",
                    "parameter": ["-ug3"],
                    "return_code": 1,
                    "run_time": 0.2053060531616211,
                    "stderr": [
                        "ERROR: MAPSET PERMANENT not found at /actinia_core/workspace/temp_db/gisdbase_ca5a55304b4d4417969499dd69ca4c24/{location_name}",
                        "",
                    ],
                    "stdout": "",
                }
            ],
            "progress": {"num_of_steps": 2, "step": 1},
            "queue": "local",
            "resource_id": "resource_id-8542d565-7f49-4a45-b8a1-3eef4888a265",
            "status": "error",
            "time_delta": 0.3622863292694092,
            "timestamp": 1711971939.483177,
            "urls": {
                "resources": [],
                "status": "https://localhost:8088/api/v3/resources/actinia-gdi/resource_id-8542d565-7f49-4a45-b8a1-3eef4888a265",
            },
            "user_id": "actinia-gdi",
        }

    @staticmethod
    def create_location(location_name, epsg):
        """Mock response for creating a location at POST: /locations/:location_name"""
        return {
            "accept_datetime": "2024-04-01 23:36:30.493092",
            "accept_timestamp": 1712014590.4930887,
            "api_info": {
                "endpoint": "locationmanagementresourceadminuser",
                "method": "POST",
                "path": f"/api/v3/locations/{location_name}",
                "request_url": f"http://localhost:8088/api/v3/locations/{location_name}",
            },
            "datetime": "2024-04-01 23:36:31.150257",
            "http_code": 200,
            "message": f"Location <{location_name}> successfully created",
            "process_chain_list": [
                {
                    "1": {
                        "flags": "t",
                        "inputs": {"epsg": epsg, "location": location_name},
                        "module": "g.proj",
                    }
                }
            ],
            "process_log": [
                {
                    "executable": "g.proj",
                    "id": "1",
                    "parameter": [f"epsg={epsg}", f"location={location_name}", "-t"],
                    "return_code": 0,
                    "run_time": 0.3056001663208008,
                    "stderr": [
                        f"Location <{location_name}> created",
                        "You can switch to the new location by",
                        f"`g.mapset mapset=PERMANENT location={location_name}`",
                        "",
                    ],
                    "stdout": "",
                }
            ],
            "process_results": {},
            "progress": {"num_of_steps": 1, "step": 1},
            "queue": "local",
            "resource_id": "resource_id-f8966bac-c813-4227-936f-44d9b006dda6",
            "status": "finished",
            "time_delta": 0.6576573848724365,
            "timestamp": 1712014591.1499546,
            "urls": {
                "resources": [],
                "status": "https://localhost:8088/api/v3/resources/actinia-gdi/resource_id-f8966bac-c813-4227-936f-44d9b006dda6",
            },
            "user_id": "actinia-gdi",
        }

    @staticmethod
    def create_location_error(location_name, epsg):
        """Mock error response for creating a location at POST: /locations/:location_name"""
        return {
            "accept_datetime": "2024-04-01 23:38:43.641825",
            "accept_timestamp": 1712014723.6418216,
            "api_info": {
                "endpoint": "locationmanagementresourceadminuser",
                "method": "POST",
                "path": f"/api/v3/locations/{location_name}",
                "request_url": f"http://localhost:8088/api/v3/locations/{location_name}",
            },
            "datetime": "2024-04-01 23:38:43.649944",
            "http_code": 400,
            "message": f"Unable to create location. Location <{location_name}> exists in user database.",
            "process_chain_list": [],
            "process_results": {},
            "queue": "local",
            "resource_id": "resource_id-a75f59a2-33df-487d-885a-73d2f53dff05",
            "status": "error",
            "time_delta": 0.008140802383422852,
            "timestamp": 1712014723.6499417,
            "urls": {
                "resources": [],
                "status": "https://localhost:8088/api/v3/resources/actinia-gdi/resource_id-a75f59a2-33df-487d-885a-73d2f53dff05",
            },
            "user_id": "actinia-gdi",
        }

    @staticmethod
    def delete_location(location_name):
        """Mock response for deleting a location at DELETE: /locations/:location_name"""
        return {"message": f"location {location_name} deleted", "status": "success"}

    @staticmethod
    def delete_location_error(location_name):
        """Mock error response for deleting a location at DELETE: /locations/:location_name"""
        return {
            "message": f"location {location_name} does not exists",
            "status": "error",
        }
