from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from grass.views.general.locations import LocationViewSet


class LocationViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LocationViewSet.as_view({"get": "list", "post": "create"})
        self.location_data = {
            "name": "Test Location",
            "latitude": 123.456,
            "longitude": 789.012,
        }

    def test_list_locations(self):
        request = self.factory.get("/locations/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_location(self):
        request = self.factory.post("/locations/", self.location_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_location(self):
        # Assuming you have a location with id=1 in the database
        request = self.factory.get("/locations/1/")
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_location(self):
        # Assuming you have a location with id=1 in the database
        request = self.factory.put("/locations/1/", self.location_data)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_location(self):
        # Assuming you have a location with id=1 in the database
        request = self.factory.patch("/locations/1/", self.location_data)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_location(self):
        # Assuming you have a location with id=1 in the database
        request = self.factory.delete("/locations/1/")
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
