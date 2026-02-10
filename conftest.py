import django
import pytest
from django.conf import settings
from django.contrib.auth.models import Group


def pytest_configure():
    settings.DJANGO_SETTINGS_MODULE = "config.settings.development"
    django.setup()


@pytest.fixture
def client_group(db):
    group, _ = Group.objects.get_or_create(name="clients")
    return group


@pytest.fixture
def user(db):
    from apps.accounts.factories import UserFactory

    return UserFactory()


@pytest.fixture
def staff_user(db):
    from apps.accounts.factories import StaffUserFactory

    return StaffUserFactory()


@pytest.fixture
def client_user(db, client_group):
    from apps.accounts.factories import UserFactory

    u = UserFactory()
    u.groups.add(client_group)
    return u
