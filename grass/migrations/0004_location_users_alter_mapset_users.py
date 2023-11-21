# Generated by Django 4.2.7 on 2023-11-14 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("grass", "0003_mapset_users"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="users",
            field=models.ManyToManyField(
                related_name="locations", to="grass.actiniauser"
            ),
        ),
        migrations.AlterField(
            model_name="mapset",
            name="users",
            field=models.ManyToManyField(
                related_name="mapsets", to="grass.actiniauser"
            ),
        ),
    ]