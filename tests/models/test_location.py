from django.test import TransactionTestCase
from django.contrib.auth.models import User
from grass.models import Location, ActiniaUser
from grass.models.enums import RolesEnum
from unittest.mock import patch
from ..mocks.ActiniaUsersAPIMocks import ActiniaUsersAPIMocks
from ..mocks.ActiniaLocationsMocks import ActiniaLocationsAPIMocks


class LocationTestCase(TransactionTestCase):
    @patch("actinia_openapi_python_client.UserManagementApi.users_user_id_post")
    @patch(
        "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
    )
    def setUp(self, mock_users_user_id_post, mock_locations_location_name_post):
        self.username = "testuser99"
        self.location_name = "TestLocation"
        self.location_epsg = 3358
        self.user_password = "testpassword"

        mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user(
            self.username
        )
        mock_locations_location_name_post.return_value = (
            ActiniaLocationsAPIMocks.create_location(
                self.location_name, self.location_epsg
            )
        )
        self.user = User.objects.create_user(
            username=self.username, password=self.user_password
        )

        self.actinia_user = self.user.actinia_user

        self.location = Location.objects.create(
            name=self.location_name, epsg=self.location_epsg, owner=self.user
        )
        self.location.actinia_users.set([self.actinia_user])
        self.location.save()

    def test_location_creation(self):
        self.assertEqual(self.location.name, self.location_name)
        self.assertEqual(self.location.epsg, self.location_epsg)
        self.assertEqual(self.location.owner, self.user)

    def test_location_str(self):
        self.assertEqual(str(self.location), self.location_name)

    def test_actinia_users_set(self):
        # Retrieve the related actinia_users for the location
        related_users = self.location.actinia_users.all()

        # Assert that the related users contain the expected actinia_user
        self.assertIn(self.actinia_user, related_users)

        # Optionally, assert that there is exactly one related user
        self.assertEqual(related_users.count(), 1)

    # def test_location_unique_constraint(self):
    #     with self.assertRaises(Exception):
    #         Location.objects.create(name="Test Location", epsg=3358, owner=self.user)
