from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.test import TransactionTestCase
from unittest.mock import patch
from ..mocks.ActiniaUsersAPIMocks import ActiniaUsersAPIMocks
from ..mocks.ActiniaLocationsMocks import ActiniaLocationsAPIMocks


class LocationAPITestCase(APITestCase, URLPatternsTestCase, TransactionTestCase):
    urlpatterns = [
        path("api/v1/", include("grass.urls")),
    ]

    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_post")
    def setUp(self, mock_users_user_id_post):
        # Create a user to authenticate requests
        mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user(
            "testuser"
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Log in the user to generate an auth token or session
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Define some data for the tests
        self.location_data = {
            "id": 0,
            "name": "Test_Location",
            "epsg": "4326",
            "public": True,
            "description": "Test Description",
            "actinia_users": [],
        }
        # URL for the API endpoint
        self.url = reverse(
            "grass:location-list"
        )  # Assuming your API uses DRF router URLs

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_get")
    def test_create_location(
        self, mock_locations_location_name_post, mock_users_user_id_get
    ):
        """Test the POST request for creating a location"""

        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location(
                self.location_data["name"], self.location_data["epsg"]
            )
        )

        mock_users_user_id_get.return_value = ActiniaUsersAPIMocks.get_user(
            self.user.username, as_dict=False
        )

        response = self.client.post(self.url, self.location_data, format="json")
        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the location was created with the correct data
        self.assertEqual(response.data["name"], self.location_data["name"])

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_info_get"
    )
    def test_get_location(self, mock_locations_location_name_info_get):
        """Test retrieving the list of locations (GET request)"""

        mock_locations_location_name_info_get.return_value = (
            ActiniaLocationsAPIMocks.get_location_info(self.location_data["name"])
        )

        response = self.client.get(self.url)

        # Ensure the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the returned data
        self.assertGreaterEqual(
            len(response.data), 1
        )  # At least one location should exist

    def test_update_location(self):
        """Test updating a location (PUT request)"""
        # First, create a location
        response = self.client.put(self.url, self.location_data, format="json")

        # Check if the location was updated correctly
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_delete"
    )
    @patch("actinia_openapi_python_client.LocationManagementApi.locations_get")
    def test_delete_location(
        self,
        mock_locations_location_name_post,
        mock_locations_location_name_delete,
        mock_locations_get,
    ):
        """Test deleting a location (DELETE request)"""

        # Mock the get locations response
        mock_locations_get.return_value = ActiniaLocationsAPIMocks.get_locations(
            location_list=[]
        )

        # Mock the create location response
        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location(
                self.location_data["name"], self.location_data["epsg"]
            )
        )

        # Mock the delete location response
        mock_locations_location_name_delete.return_value = (
            ActiniaLocationsAPIMocks.delete_location(self.location_data["name"])
        )

        # Create a location
        response = self.client.post(self.url, self.location_data, format="json")
        location_id = response.data["id"]

        # Send a DELETE request
        url = reverse("grass:location-detail", args=[location_id])
        response = self.client.delete(url)

        # Check that the location was deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the location no longer exists
        response = self.client.get(self.url)
        print(f"test_delete_location.get: {response.data}")
        self.assertEqual(
            response.data.get("count"), 0
        )  # Assuming this was the only location
