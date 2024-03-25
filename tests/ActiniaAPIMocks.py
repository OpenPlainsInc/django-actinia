###############################################################################
# Filename: ActiniaAPIMocks.py                                                 #
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


class ActiniaAPIMocks:

    # Actinia Users Requests
    @staticmethod
    def get_users(user_list=["actinia-gdi"]):
        """Mock response for getting users at GET: /users"""
        return {"status": "success", "user_list": user_list}

    @staticmethod
    def get_user(user_id, user_role="admin"):
        """Mock response for getting a user at GET: /users/{user_id}"""
        return {
            "permissions": {
                "accessible_datasets": {},
                "accessible_modules": [
                    "d.legend",
                    "d.rast",
                    "d.rast.multi",
                    "d.vect",
                    "exporter",
                    "g.findfile",
                    "g.gisenv",
                    "g.list",
                    "g.mapset",
                    "g.proj",
                    "g.region",
                    "g.remove",
                    "g.rename",
                    "g.version",
                    "i.atcorr",
                    "i.cluster",
                    "i.colors.enhance",
                    "i.gensig",
                    "i.group",
                    "i.landsat.toar",
                    "i.maxlik",
                    "i.pansharpen",
                    "i.segment",
                    "i.tasscap",
                    "i.vi",
                    "importer",
                    "r.blend",
                    "r.buffer",
                    "r.buffer.lowmem",
                    "r.carve",
                    "r.category",
                    "r.circle",
                    "r.clump",
                    "r.coin",
                    "r.colors",
                    "r.colors.out",
                    "r.composite",
                    "r.compress",
                    "r.contour",
                    "r.cost",
                    "r.covar",
                    "r.cross",
                    "r.describe",
                    "r.distance",
                    "r.drain",
                    "r.fill.dir",
                    "r.fillnulls",
                    "r.flow",
                    "r.grow",
                    "r.grow.distance",
                    "r.gwflow",
                    "r.his",
                    "r.horizon",
                    "r.info",
                    "r.kappa",
                    "r.lake",
                    "r.latlong",
                    "r.li.cwed",
                    "r.li.dominance",
                    "r.li.edgedensity",
                    "r.li.mpa",
                    "r.li.mps",
                    "r.li.padcv",
                    "r.li.padrange",
                    "r.li.padsd",
                    "r.li.patchdensity",
                    "r.li.patchnum",
                    "r.li.pielou",
                    "r.li.renyi",
                    "r.li.richness",
                    "r.li.shannon",
                    "r.li.shape",
                    "r.li.simpson",
                    "r.mapcalc",
                    "r.mask",
                    "r.mfilter",
                    "r.mode",
                    "r.neighbors",
                    "r.null",
                    "r.out.png",
                    "r.param.scale",
                    "r.patch",
                    "r.plane",
                    "r.profile",
                    "r.proj",
                    "r.quant",
                    "r.quantile",
                    "r.random",
                    "r.random.cells",
                    "r.random.surface",
                    "r.reclass",
                    "r.reclass.area",
                    "r.recode",
                    "r.region",
                    "r.regression.line",
                    "r.regression.multi",
                    "r.regression.series",
                    "r.relief",
                    "r.report",
                    "r.resamp.bspline",
                    "r.resamp.filter",
                    "r.resamp.interp",
                    "r.resamp.rst",
                    "r.resamp.stats",
                    "r.resample",
                    "r.rescale",
                    "r.rescale.eq",
                    "r.rgb",
                    "r.ros",
                    "r.series",
                    "r.series.accumulate",
                    "r.series.interp",
                    "r.shade",
                    "r.sim.sediment",
                    "r.sim.water",
                    "r.slope.aspect",
                    "r.solute.transport",
                    "r.spread",
                    "r.spreadpath",
                    "r.statistics",
                    "r.stats",
                    "r.stats.quantile",
                    "r.stats.zonal",
                    "r.stream.extract",
                    "r.sun",
                    "r.sunhours",
                    "r.sunmask",
                    "r.support",
                    "r.support.stats",
                    "r.surf.area",
                    "r.surf.contour",
                    "r.surf.fractal",
                    "r.surf.gauss",
                    "r.surf.idw",
                    "r.surf.random",
                    "r.terraflow",
                    "r.texture",
                    "r.thin",
                    "r.tile",
                    "r.tileset",
                    "r.timestamp",
                    "r.to.rast3",
                    "r.to.rast3elev",
                    "r.to.vect",
                    "r.topidx",
                    "r.topmodel",
                    "r.transect",
                    "r.univar",
                    "r.uslek",
                    "r.usler",
                    "r.viewshed",
                    "r.vol.dem",
                    "r.volume",
                    "r.walk",
                    "r.water.outlet",
                    "r.watershed",
                    "r.what",
                    "r.what.color",
                    "t.create",
                    "t.info",
                    "t.list",
                    "t.rast.accdetect",
                    "t.rast.accumulate",
                    "t.rast.aggr_func",
                    "t.rast.aggregate",
                    "t.rast.aggregate.ds",
                    "t.rast.algebra",
                    "t.rast.colors",
                    "t.rast.extract",
                    "t.rast.gapfill",
                    "t.rast.list",
                    "t.rast.mapcalc",
                    "t.rast.sample",
                    "t.rast.series",
                    "t.rast.univar",
                    "t.rast.what",
                    "t.register",
                    "t.remove",
                    "t.unregister",
                    "v.buffer",
                    "v.clean",
                    "v.db.select",
                    "v.db.univar",
                    "v.db.update",
                    "v.dissolve",
                    "v.in.ascii",
                    "v.overlay",
                    "v.patch",
                    "v.random",
                    "v.rast.stats",
                    "v.select",
                    "v.what.rast",
                    "v.what.strds",
                ],
                "cell_limit": 1000000000,
                "process_num_limit": 1000,
                "process_time_limit": 600,
            },
            "status": "success",
            "user_group": "admin",
            "user_id": user_id,
            "user_role": user_role,
        }

    @staticmethod
    def get_user_error(user_id):
        """Mock error response for getting a user at GET: /users/{user_id}"""
        return {"message": f"User <{user_id}> does not exist", "status": "error"}

    @staticmethod
    def create_user(user_id):
        """Mock response for creating a user at POST: /users/{user_id}"""
        return {"status": "success", "message": f"User {user_id} created"}

    @staticmethod
    def create_user_error(user_id):
        """Mock error response for creating a user at POST: /users/{user_id}"""
        return {"status": "error", "message": f"User <{user_id}> already exists"}

    @staticmethod
    def delete_user(user_id):
        """Mock response for deleting a user at DELETE: /users/{user_id}"""
        return {"status": "success", "message": f"User {user_id} deleted"}

    @staticmethod
    def delete_user_error(user_id):
        """Mock error response for deleting a user at DELETE: /users/{user_id}"""
        return {
            "message": f"Unable to delete user {user_id}. User does not exist.",
            "status": "error",
        }
