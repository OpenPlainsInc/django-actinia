from django.test import TestCase
from grass.serializers.InputParameterImportDescrSerializer import (
    InputParameterImportDescrSerializer,
)


class TestInputParameterImportDescrSerializer(TestCase):
    def test_InputParameterImportDescrSerializer(self):
        data = [
            {
                "type": "raster",
                "source": "http://example.com/raster.tif",
                "resample": "bilinear",
                "resolution": "estimated",
            },
            {
                "type": "vector",
                "source": "http://example.com/vector.shp",
                "extent": "10,20,30,40",
                "filter": "attribute='value'",
            },
            {
                "type": "landsat",
                "source": "LT52170762005240COA00",
                "landsat_atcor": "dos1",
                "semantic_label": "red",
            },
        ]

        for item in data:
            serializer = InputParameterImportDescrSerializer(data=item)
            self.assertTrue(serializer.is_valid())
