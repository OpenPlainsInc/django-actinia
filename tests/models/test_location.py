from django.test import TestCase
from django.contrib.auth.models import User
from grass.models import Location, ActiniaUser
from grass.models.enums import RolesEnum
from unittest.mock import patch
from ..mocks.ActiniaUsersAPIMocks import ActiniaUsersAPIMocks
from ..mocks.ActiniaLocationsMocks import ActiniaLocationsAPIMocks


class LocationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "testuser99"
        cls.location_name = "TestLocation"
        cls.location_epsg = 3358
        cls.user_password = "testpassword"

        with patch(
            "actinia_openapi_python_client.UserManagementApi.users_user_id_post"
        ) as mock_users_user_id_post, patch(
            "actinia_openapi_python_client.LocationManagementApi.locations_location_name_post"
        ) as mock_locations_location_name_post:
            mock_users_user_id_post.return_value = ActiniaUsersAPIMocks.create_user(
                cls.username
            )
            mock_locations_location_name_post.return_value = (
                ActiniaLocationsAPIMocks.create_location(
                    cls.location_name, cls.location_epsg
                )
            )
            cls.user = User.objects.create_user(
                username=cls.username, password=cls.user_password
            )
            cls.actinia_user = ActiniaUser.objects.create(
                user=cls.user, actinia_role=RolesEnum.ADMIN.value
            )

            cls.location = Location.objects.create(
                name=cls.location_name, epsg=cls.location_epsg, owner=cls.user
            )
            cls.location.actinia_users.set([cls.actinia_user])
            cls.location.save()

    @classmethod
    def tearDownClass(cls):
        with patch(
            "actinia_openapi_python_client.LocationManagementApi.locations_location_name_delete"
        ) as mock_locations_location_name_delete, patch(
            "actinia_openapi_python_client.UserManagementApi.users_user_id_delete"
        ) as mock_users_user_id_delete:
            mock_locations_location_name_delete.return_value = (
                ActiniaLocationsAPIMocks.delete_location(cls.location_name)
            )
            cls.location.delete()
            mock_users_user_id_delete.return_value = ActiniaUsersAPIMocks.delete_user(
                cls.username
            )
            cls.actinia_user.delete()
            cls.user.delete()

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
