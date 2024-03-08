from django.test import TestCase
from django.contrib.auth.models import User
from grass.models import Location, ActiniaUser
from grass.models.enums import RolesEnum


class LocationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser99", password="testpassword"
        )
        actinia_user = ActiniaUser.objects.create_actinia_user(
            user=self.user, actinia_role=RolesEnum.ADMIN.value
        )
        self.location = Location(name="Test Location", epsg=3358, owner=self.user)
        self.location.actinia_users.set(actinia_user)
        self.location.save()

    def test_location_creation(self):
        self.assertEqual(self.location.name, "Test Location")
        self.assertEqual(self.location.epsg, 3358)
        self.assertEqual(self.location.owner, self.user)

    def test_location_str(self):
        self.assertEqual(str(self.location), "Test Location")

    def test_location_unique_constraint(self):
        with self.assertRaises(Exception):
            Location.objects.create(name="Test Location", epsg=4326, owner=self.user)
