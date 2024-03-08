from django.test import TestCase
from django.contrib.auth.models import User
from grass.models import Location, ActiniaUser
from grass.models.enums import RolesEnum


class LocationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser99", password="testpassword"
        )
        cls.actinia_user = ActiniaUser.objects.create_actinia_user(
            user=cls.user, actinia_role=RolesEnum.ADMIN.value
        )
        cls.location = Location.objects.create(
            name="TestLocation", epsg=3358, owner=cls.user
        )
        cls.location.actinia_users.set([cls.actinia_user])
        cls.location.save()

    @classmethod
    def tearDownClass(cls):
        cls.location.delete()
        cls.actinia_user.delete()
        cls.user.delete()

    def test_location_creation(self):
        self.assertEqual(self.location.name, "TestLocation")
        self.assertEqual(self.location.epsg, 3358)
        self.assertEqual(self.location.owner, self.user)

    def test_location_str(self):
        self.assertEqual(str(self.location), "TestLocation")

    # def test_location_unique_constraint(self):
    #     with self.assertRaises(Exception):
    #         Location.objects.create(name="Test Location", epsg=3358, owner=self.user)
