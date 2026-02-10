import pytest
from django.contrib.auth.models import Group
from django.test import Client

from apps.accounts.factories import StaffUserFactory, UserFactory
from apps.portal.factories import ClientProjectFactory, MessageFactory
from apps.portal.models import Message
from apps.projects.factories import ProjectFactory


@pytest.fixture
def client_group(db):
    group, _ = Group.objects.get_or_create(name="clients")
    return group


def make_client_user(client_group):
    user = UserFactory()
    user.groups.add(client_group)
    return user


@pytest.mark.django_db
class TestPortalDashboard:
    def test_anon_redirects(self):
        c = Client()
        response = c.get("/portail/")
        assert response.status_code == 302

    def test_regular_user_403(self):
        user = UserFactory()
        c = Client()
        c.force_login(user)
        response = c.get("/portail/")
        assert response.status_code == 403

    def test_client_200(self, client_group):
        user = make_client_user(client_group)
        c = Client()
        c.force_login(user)
        response = c.get("/portail/")
        assert response.status_code == 200

    def test_staff_sees_all(self):
        staff = StaffUserFactory()
        ProjectFactory()
        ProjectFactory()
        c = Client()
        c.force_login(staff)
        response = c.get("/portail/")
        assert response.status_code == 200
        assert len(response.context["projects"]) == 2

    def test_client_sees_only_assigned(self, client_group):
        user = make_client_user(client_group)
        p1 = ProjectFactory()
        ProjectFactory()
        ClientProjectFactory(user=user, project=p1)
        c = Client()
        c.force_login(user)
        response = c.get("/portail/")
        projects = list(response.context["projects"])
        assert len(projects) == 1
        assert projects[0] == p1


@pytest.mark.django_db
class TestPortalProjectDetail:
    def test_client_no_access_403(self, client_group):
        user = make_client_user(client_group)
        p = ProjectFactory(slug="restricted")
        c = Client()
        c.force_login(user)
        response = c.get(f"/portail/projets/{p.slug}/")
        assert response.status_code == 403

    def test_client_with_access_200(self, client_group):
        user = make_client_user(client_group)
        p = ProjectFactory(slug="accessible")
        ClientProjectFactory(user=user, project=p)
        c = Client()
        c.force_login(user)
        response = c.get(f"/portail/projets/{p.slug}/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestPortalMessages:
    def test_message_list_scoped_to_user(self, client_group):
        user = make_client_user(client_group)
        other = UserFactory()
        msg_to_user = MessageFactory(to_user=user, from_user=other)
        msg_to_other = MessageFactory(to_user=other, from_user=user)
        c = Client()
        c.force_login(user)
        response = c.get("/portail/messages/")
        messages = list(response.context["messages"])
        assert msg_to_user in messages
        assert msg_to_other not in messages

    def test_message_detail_auto_marks_read(self, client_group):
        user = make_client_user(client_group)
        msg = MessageFactory(to_user=user, read=False)
        c = Client()
        c.force_login(user)
        c.get(f"/portail/messages/{msg.pk}/")
        msg.refresh_from_db()
        assert msg.read is True

    def test_compose_sets_from_user(self, client_group):
        user = make_client_user(client_group)
        staff = StaffUserFactory()
        c = Client()
        c.force_login(user)
        response = c.post(
            "/portail/messages/nouveau/",
            {"to_user": staff.pk, "subject": "Test", "content": "Bonjour"},
        )
        assert response.status_code == 302
        msg = Message.objects.filter(from_user=user).first()
        assert msg is not None
        assert msg.to_user == staff

    def test_mark_as_read_get_not_allowed(self, client_group):
        user = make_client_user(client_group)
        msg = MessageFactory(to_user=user, read=False)
        c = Client()
        c.force_login(user)
        response = c.get(f"/portail/messages/{msg.pk}/lu/")
        assert response.status_code == 405

    def test_mark_as_read_post_204(self, client_group):
        user = make_client_user(client_group)
        msg = MessageFactory(to_user=user, read=False)
        c = Client()
        c.force_login(user)
        response = c.post(f"/portail/messages/{msg.pk}/lu/")
        assert response.status_code == 204
        msg.refresh_from_db()
        assert msg.read is True


@pytest.mark.django_db
class TestDocumentDownload:
    def test_client_no_access_403(self, client_group):
        user = make_client_user(client_group)
        from apps.projects.factories import ProjectDocumentFactory
        doc = ProjectDocumentFactory()
        c = Client()
        c.force_login(user)
        response = c.get(f"/portail/projets/{doc.project.slug}/telecharger/{doc.pk}/")
        assert response.status_code == 403

    def test_staff_can_download(self):
        staff = StaffUserFactory()
        from apps.projects.factories import ProjectDocumentFactory
        doc = ProjectDocumentFactory()
        c = Client()
        c.force_login(staff)
        response = c.get(f"/portail/projets/{doc.project.slug}/telecharger/{doc.pk}/")
        assert response.status_code == 302

    def test_client_with_access_can_download(self, client_group):
        user = make_client_user(client_group)
        from apps.projects.factories import ProjectDocumentFactory
        doc = ProjectDocumentFactory()
        ClientProjectFactory(user=user, project=doc.project)
        c = Client()
        c.force_login(user)
        response = c.get(f"/portail/projets/{doc.project.slug}/telecharger/{doc.pk}/")
        assert response.status_code == 302
