import pytest

from apps.accounts.factories import UserFactory
from apps.accounts.models import Profile


@pytest.mark.django_db
class TestProfileSignal:
    def test_profile_created_on_user_create(self):
        user = UserFactory()
        assert Profile.objects.filter(user=user).exists()

    def test_profile_not_duplicated_on_update(self):
        user = UserFactory()
        user.first_name = "Updated"
        user.save()
        assert Profile.objects.filter(user=user).count() == 1

    def test_profile_recreated_if_missing(self):
        user = UserFactory()
        Profile.objects.filter(user=user).delete()
        assert not Profile.objects.filter(user=user).exists()
        user.first_name = "Trigger"
        user.save()
        assert Profile.objects.filter(user=user).exists()
