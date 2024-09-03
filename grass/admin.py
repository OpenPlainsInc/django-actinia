###############################################################################
# Filename: admin.py                                                           #
# Project: OpenPlains Inc.                                                     #
# File Created: Monday June 6th 2022                                           #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Sep 03 2024                                               #
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
from django.contrib.contenttypes.models import ContentType

# from django.contrib.contenttypes.admin import ContentTypeAdmin
from .models import ActiniaUser, Location, Mapset, Region, Token, Layer, Permission


# class LocationInline(admin.TabularInline):
#     model = Location
#     extra = 0

# Unregister the existing ContentType admin
# admin.site.unregister(ContentType)


class MapsetInline(admin.TabularInline):
    model = Mapset
    extra = 1
    show_change_link = True


class LayerInline(admin.TabularInline):
    model = Layer
    extra = 1
    show_change_link = True


@admin.register(ActiniaUser)
class ActiniaUserAdmin(admin.ModelAdmin):
    list_display = ("actinia_username", "actinia_role", "user", "api_token")
    list_filter = ("actinia_username", "actinia_role", "user")
    search_fields = ("actinia_username", "user", "role")
    # inlines = [LocationInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "owner", "epsg", "public", "slug")
    list_filter = ("name", "description", "owner", "epsg", "public")
    search_fields = ("name", "description", "owner", "epsg", "public")
    inlines = []

    def get_inlines(self, request, obj):
        if obj:
            return [MapsetInline]
        return []

    # inlines = [MapsetInline]


@admin.register(Mapset)
class MapsetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_on",
        "created_by",
        "updated_on",
        "updated_by",
        "name",
        "description",
        "owner",
        "public",
        "slug",
        "project",
    )
    list_filter = (
        "created_on",
        "created_by",
        "updated_on",
        "updated_by",
        "owner",
        "public",
        "project",
    )
    autocomplete_fields = ("owner", "project", "allowed_users")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ["name"]}

    inlines = []

    def get_inlines(self, request, obj):
        if obj:
            return [LayerInline]
        return []


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        "actinia_user",
        "action",
        "content_type",
        "object_id",
        "start_time",
        "end_time",
        "day_of_week",
    )
    list_filter = ("action", "day_of_week")
    search_fields = ("actinia_user__user__username", "content_type__model", "object_id")
    autocomplete_fields = ("actinia_user", "content_type")

    fieldsets = (
        (None, {"fields": ("actinia_user", "action", "content_type", "object_id")}),
        (
            "When Clause",
            {
                "fields": ("start_time", "end_time", "day_of_week", "custom_condition"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    search_fields = ("model", "app_label")


class TokenAdmin(admin.ModelAdmin):
    list_display = ("token", "actinia_user", "expires", "user", "api_key")


# Register ContentType for autocomplete functionality
# admin.site.register(ContentType)

# admin.site.register(ActiniaUser, ActiniaUserAdmin)
# admin.site.register(Location, LocationAdmin)
# admin.site.register(Token, TokenAdmin)
