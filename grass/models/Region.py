from django.db import models


class Region(models.Model):
    """
    A Django model representing a geographic region.

    Attributes:
        zone (integer): The zone of the region.
        projection (integer): The projection of the region.
        n (float): The northern boundary of the region.
        s (float): The southern boundary of the region.
        e (float): The eastern boundary of the region.
        w (float): The western boundary of the region.
        t (float): The top boundary of the region.
        b (float): The bottom boundary of the region.
        nsres (float): The north-south resolution of the region.
        ewres (float): The east-west resolution of the region.
        nsres3 (float): The north-south resolution of the region in 3D.
        ewres3 (float): The east-west resolution of the region in 3D.
        tbres (float): The top-bottom resolution of the region.
        rows (float): The number of rows in the region.
        cols (float): The number of columns in the region.
        rows3 (float): The number of rows in the region in 3D.
        cols3 (float): The number of columns in the region in 3D.
        depths (float): The depth of the region.
        cells (float): The number of cells in the region.
        cells3 (float): The number of cells in the region in 3D.
    """

    zone = models.IntegerField()
    projection = models.IntegerField()
    n = models.FloatField()
    s = models.FloatField()
    e = models.FloatField()
    w = models.FloatField()
    t = models.FloatField()
    b = models.FloatField()
    nsres = models.FloatField()
    ewres = models.FloatField()
    nsres3 = models.FloatField()
    ewres3 = models.FloatField()
    tbres = models.FloatField()
    rows = models.FloatField()
    cols = models.FloatField()
    rows3 = models.FloatField()
    cols3 = models.FloatField()
    depths = models.FloatField()
    cells = models.FloatField()
    cells3 = models.FloatField()
