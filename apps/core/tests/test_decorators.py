import pytest
from django.contrib.auth.models import AnonymousUser, Group
from django.http import HttpResponse
from django.test import RequestFactory

from apps.accounts.factories import UserFactory
from apps.core.decorators import admin_required, client_required


def dummy_view(request):
    return HttpResponse("OK")


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.mark.django_db
class TestClientRequired:
    def test_anon_redirects_to_login(self, rf):
        request = rf.get("/test/")
        request.user = AnonymousUser()
        response = client_required(dummy_view)(request)
        assert response.status_code == 302
        assert "/comptes/" in response.url or "/accounts/" in response.url

    def test_regular_user_redirects_home(self, rf):
        request = rf.get("/test/")
        request.user = UserFactory()
        response = client_required(dummy_view)(request)
        assert response.status_code == 302
        assert response.url == "/"

    def test_client_group_passes(self, rf):
        user = UserFactory()
        group, _ = Group.objects.get_or_create(name="clients")
        user.groups.add(group)
        request = rf.get("/test/")
        request.user = user
        response = client_required(dummy_view)(request)
        assert response.status_code == 200

    def test_staff_passes(self, rf):
        request = rf.get("/test/")
        request.user = UserFactory(is_staff=True)
        response = client_required(dummy_view)(request)
        assert response.status_code == 200


@pytest.mark.django_db
class TestAdminRequired:
    def test_non_staff_redirects(self, rf):
        request = rf.get("/test/")
        request.user = UserFactory(is_staff=False)
        response = admin_required(dummy_view)(request)
        assert response.status_code == 302
        assert response.url == "/"

    def test_staff_passes(self, rf):
        request = rf.get("/test/")
        request.user = UserFactory(is_staff=True)
        response = admin_required(dummy_view)(request)
        assert response.status_code == 200
