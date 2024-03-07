from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from grass.serializers.UrlModelSerializer import UrlModelSerializer


class UrlModelSerializerTest(TestCase):
    def test_url_model_serializer_fields(self):
        serializer = UrlModelSerializer()
        expected_fields = ["status", "resources"]
        for field_name in expected_fields:
            self.assertIn(field_name, serializer.fields)
            field = serializer.fields[field_name]
            self.assertIsInstance(field, serializers.Field)
