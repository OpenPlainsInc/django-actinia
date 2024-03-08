###############################################################################
# Filename: admin.py                                                           #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday June 6th 2022                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Mon Nov 27 2023                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2023 OpenPlains Inc.                                                #
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

from django.contrib import admin

from .models import ActiniaUser, Location, Mapset, Region, Token


class LocationInline(admin.TabularInline):
    model = Location
    extra = 0


class MapsetInline(admin.TabularInline):
    model = Mapset
    extra = 0


class ActiniaUserAdmin(admin.ModelAdmin):
    list_display = ("actinia_username", "actinia_role", "user")
    list_filter = ("actinia_username", "actinia_role", "user")

    # inlines = [LocationInline]


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "owner", "epsg", "public")
    list_filter = ("name", "description", "owner", "epsg", "public")

    # inlines = [MapsetInline]


class MapsetAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "owner", "location")
    list_filter = ("name", "description", "owner", "location")

    # inlines = [LocationInline]


class TokenAdmin(admin.ModelAdmin):
    list_display = ("token", "actinia_user", "expires", "user", "api_key")


admin.site.register(ActiniaUser, ActiniaUserAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Mapset, MapsetAdmin)
admin.site.register(Token, TokenAdmin)
