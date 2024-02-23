###############################################################################
# Filename: urls.py                                                            #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday June 6th 2022                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Thu Jan 11 2024                                               #
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


from django.urls import path, include
from rest_framework import routers
from django.views.decorators.cache import cache_page


from grass.views.general import locations

# from grass.views.ActiniaUserView import ActiniaUserView
from grass.views.ActiniaUserViewSet import ActiniaUserViewSet
from grass.views.general.locations import LocationViewSet
from grass.views.general.mapsets import MapsetViewSet

# from views.raster import raster
# from views import vector
# from views import imagery


from rest_framework.routers import DefaultRouter


app_name = "grass"

router = DefaultRouter()
router.register(
    r"actinia-user/(?P<task>\w+)",
    ActiniaUserViewSet,
    basename="actinia-user",
)

router.register(r"locations", LocationViewSet, basename="location")

router.register(
    r"locations/(?P<location_pk>\d+)/mapsets", MapsetViewSet, basename="mapset"
)

urlpatterns = [
    path("", include(router.urls)),
    # path('locations/', LocationList.as_view(), name='location-list'),
    # path("users/", ActiniaUserView.as_view(), name="users"),
    # path("api-log/<str:user_id>/", ActiniaUserView.as_view(), name="api-log"),
    ## General (g)
    # path(
    #     "g/locations/",
    #     cache_page(60 * 15, key_prefix="grass_locations")(
    #         locations.LocationList.as_view()
    #     ),
    #     name="ListLocations",
    # ),
    # path("g/locations/<str:location_name>", locations.gLocations, name="Location"),
    # path('g/locations/<str:location_name>/info', cache_page(60 * 15)(views.gLocationInfo), name="LocationInfo"),
    # path('g/locations/<str:location_name>/mapsets', views.gMapsets, name="Mapsets"),
    # path('g/locations/<str:location_name>/mapsets/<str:mapset_name>', views.gMapset, name="Mapset"),
    # path('g/locations/<str:location_name>/mapsets/<str:mapset_name>/info', cache_page(60 * 15)(views.gMapsetInfo), name="MapsetInfo"),
    # path('g/locations/<str:location_name>/mapsets/<str:mapset_name>/raster_layers', cache_page(60 * 15)(views.gListRasters), name="ListRaster"),
    # path('g/locations/<str:location_name>/mapsets/<str:mapset_name>/vector_layers', cache_page(60 * 15)(views.gListVectors), name="ListVector"),
    # path('g/modules', cache_page(60 * 15)(views.gModules), name="gModules"),
    # path('g/modules/<str:grassmodule>', cache_page(60 * 15)(views.gModule), name="gModule"),
    ## Raster (r)
    # path('r/locations/<str:location_name>/mapsets/<str:mapset_name>/raster_layers/<str:raster_name>', cache_page(60 * 15)(views.rInfo), name="rInfo"),
    # path('r/locations/<str:location_name>/mapsets/<str:mapset_name>/raster_layers/<str:raster_name>/render', cache_page(60 * 15)(views.rRenderImage), name="renderRaster"),
    # path('r/locations/<str:location_name>/mapsets/<str:mapset_name>/raster_layers/<str:raster_name>/colors', cache_page(60 * 15)(views.rColors), name="rColors"),
    # path('r/locations/<str:location_name>/mapsets/<str:mapset_name>/raster_layers/<str:raster_name>/geotiff_async_orig', views.rGeoTiff, name="rGeoTiff"),
    ## Raster Stats
    # path('r/locations/<str:location_name>/mapsets/<str:mapset_name>/raster_layers/<str:raster_name>/area_stats_async', cache_page(60 * 15)(views.rRenderImage), name="area_stats_async"),
    # path('r/locations/<str:location_name>/mapsets/<str:mapset_name>/raster_layers/<str:raster_name>/area_stats_sync', cache_page(60 * 15)(views.rRenderImage), name="area_stats_sync"),
    # path('r/locations/<str:location_name>/mapsets/<str:mapset_name>/raster_layers/<str:raster_name>/area_stats_univar_async', cache_page(60 * 15)(views.rRenderImage), name="area_stats_univar_async"),
    # path('r/locations/<str:location_name>/mapsets/<str:mapset_name>/raster_layers/<str:raster_name>/area_stats_univar_sync', cache_page(60 * 15)(views.rRenderImage), name="area_stats_univar_sync"),
    # path('r/resource/<str:raster_name>/stream/<str:resource_id>', views.streamCOG, name="rStreamOCG"),
    # path('v/locations/<str:location_name>/mapsets/<str:mapset_name>/vector_layers/<str:vector_name>', cache_page(60 * 15)(views.vInfo), name="vInfo"),
    # path('v/locations/<str:location_name>/mapsets/<str:mapset_name>/vector_layers/<str:vector_name>/render', cache_page(60 * 15)(views.vRenderImage), name="renderVector"),
    # path('v/locations/<str:location_name>/mapsets/<str:mapset_name>/vector_layers/<str:vector_name>/sampling_async', cache_page(60 * 15)(views.rColors), name="vSamplingAsync"),
    # path('v/locations/<str:location_name>/mapsets/<str:mapset_name>/vector_layers/<str:vector_name>/sampling_sync', views.rGeoTiff, name="vSamplingSync"),
    # path('i', views.ping, name='i')
]
