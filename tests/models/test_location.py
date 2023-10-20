from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from actinia.models import Location, Organization

# from django.contrib.auth.models import User
from django.db import transaction


class TestLocationModel(TestCase):
    @transaction.atomic
    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.force_login(self.user)

        self.organization = Organization.objects.create(
            name="test_organization", owner=self.user
        )

    # @transaction.atomic
    # def tearDown(self):
    #     Location.objects.all().delete()
    #     Organization.objects.all().delete()
    #     User.objects.all().delete()

    def test_location_creation(self):
        location = Location.objects.create(
            name="test_location",
            description="test_description",
            owner=self.user,
            epsg="3358",
            public=False,
            organization=self.organization,
        )
        assert location.owner == self.user
        assert location.description == "test_description"

    def test_location_public_default(self):
        location = Location.objects.create(
            name="test_location",
            epsg="4326",
            owner=self.user,
            organization=self.organization,
        )
        assert location.public is False

    def test_location_str(self):
        location = Location.objects.create(
            name="test_location",
            public=False,
            owner=self.user,
            organization=self.organization,
        )
        assert str(location) == "test_location"
