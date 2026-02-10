import pytest
from django.contrib.auth.models import Group

from apps.accounts.factories import UserFactory
from apps.accounts.models import User


@pytest.mark.django_db
class TestUserSoftDelete:
    def test_delete_sets_is_deleted(self):
        user = UserFactory()
        user.delete()
        user.refresh_from_db()
        assert user.is_deleted is True
        assert user.deleted_at is not None
        assert user.is_active is False

    def test_soft_deleted_excluded_from_default_manager(self):
        user = UserFactory()
        user.delete()
        assert user not in User.objects.all()

    def test_all_objects_includes_deleted(self):
        user = UserFactory()
        user.delete()
        assert user in User.all_objects.all()

    def test_hard_delete_removes_from_db(self):
        user = UserFactory()
        pk = user.pk
        user.hard_delete()
        assert not User.all_objects.filter(pk=pk).exists()

    def test_restore_reverts_soft_delete(self):
        user = UserFactory()
        user.delete()
        user.restore()
        user.refresh_from_db()
        assert user.is_deleted is False
        assert user.deleted_at is None
        assert user.is_active is True
        assert user in User.objects.all()


@pytest.mark.django_db
class TestProfileRole:
    def test_role_admin(self):
        user = UserFactory(is_staff=True)
        assert user.profile.role == "admin"

    def test_role_client(self):
        user = UserFactory()
        group, _ = Group.objects.get_or_create(name="clients")
        user.groups.add(group)
        assert user.profile.role == "client"

    def test_role_guest(self):
        user = UserFactory()
        assert user.profile.role == "guest"

    def test_profile_str_with_name(self):
        user = UserFactory(first_name="Moussa", last_name="Ibrahim")
        assert str(user.profile) == "Moussa Ibrahim"

    def test_profile_str_fallback_email(self):
        user = UserFactory(first_name="", last_name="")
        assert str(user.profile) == user.email
