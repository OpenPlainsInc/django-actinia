# Generated by Django 5.1 on 2024-09-03 15:52

import django.contrib.gis.db.models.fields
import django.db.models.deletion
import grass.models.fields.LayerTypeEnumField
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("grass", "0009_remove_location_unique_location_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="mapset",
            old_name="location",
            new_name="project",
        ),
        migrations.AlterUniqueTogether(
            name="mapset",
            unique_together={("name", "project", "owner")},
        ),
        migrations.AddField(
            model_name="actiniauser",
            name="api_token",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="mapset",
            name="allowed_users",
            field=models.ManyToManyField(
                related_name="accessible_mapsets", to="grass.actiniauser"
            ),
        ),
        migrations.AlterField(
            model_name="actiniauser",
            name="password",
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name="actiniauser",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="actinia_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="actinia_users",
            field=models.ManyToManyField(
                related_name="projects", to="grass.actiniauser"
            ),
        ),
        migrations.CreateModel(
            name="Layer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=150)),
                ("description", models.CharField(blank=True, max_length=250)),
                ("public", models.BooleanField(default=False)),
                (
                    "slug",
                    models.SlugField(
                        blank=True, editable=False, max_length=150, unique=True
                    ),
                ),
                ("mutable", models.BooleanField(default=False)),
                (
                    "layer_type",
                    grass.models.fields.LayerTypeEnumField(
                        choices=[
                            ("RS", "raster"),
                            ("R3", "raster_3d"),
                            ("VE", "vector"),
                            ("ST", "stdr"),
                            ("SC", "stac"),
                            ("TA", "tabular"),
                        ],
                        default="RS",
                        max_length=2,
                    ),
                ),
                ("size", models.CharField()),
                ("eres", models.FloatField()),
                ("wres", models.FloatField()),
                ("stac_asset", models.URLField()),
                ("thumbnail", models.URLField()),
                ("bbox", django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                (
                    "actinia_owner",
                    models.ManyToManyField(
                        related_name="layers", to="grass.actiniauser"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "mapset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="layers",
                        to="grass.mapset",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="mapset",
            name="users",
        ),
        migrations.CreateModel(
            name="Permission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("read", "Read"),
                            ("write", "Write"),
                            ("delete", "Delete"),
                            ("execute", "Execute"),
                        ],
                        max_length=50,
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                ("start_time", models.TimeField(blank=True, null=True)),
                ("end_time", models.TimeField(blank=True, null=True)),
                ("day_of_week", models.CharField(blank=True, max_length=9, null=True)),
                ("custom_condition", models.TextField(blank=True, null=True)),
                (
                    "actinia_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="grass.actiniauser",
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grass_permissions",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {
                    ("actinia_user", "content_type", "object_id", "action")
                },
            },
        ),
    ]