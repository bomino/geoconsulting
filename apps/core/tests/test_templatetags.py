import pytest
from django.template import Context, Template
from django.test import RequestFactory


class TestRenderMarkdown:
    def test_renders_bold(self):
        t = Template("{% load core_tags %}{{ text|markdown }}")
        out = t.render(Context({"text": "**bold**"}))
        assert "<strong>bold</strong>" in out

    def test_empty_value_returns_empty(self):
        t = Template("{% load core_tags %}{{ text|markdown }}")
        out = t.render(Context({"text": ""}))
        assert out.strip() == ""

    def test_strips_disallowed_tags(self):
        t = Template("{% load core_tags %}{{ text|markdown }}")
        out = t.render(Context({"text": "<script>alert('xss')</script>"}))
        assert "<script>" not in out


class TestActiveNav:
    def test_active_on_exact_match(self):
        factory = RequestFactory()
        request = factory.get("/")
        t = Template("{% load core_tags %}{% active_nav 'home' %}")
        out = t.render(Context({"request": request}))
        assert "text-primary-700" in out

    def test_inactive_on_different_path(self):
        factory = RequestFactory()
        request = factory.get("/contact/")
        t = Template("{% load core_tags %}{% active_nav 'home' %}")
        out = t.render(Context({"request": request}))
        assert "text-gray-600" in out

    def test_no_request_returns_inactive(self):
        t = Template("{% load core_tags %}{% active_nav 'home' %}")
        out = t.render(Context({}))
        assert "text-gray-600" in out

    def test_invalid_url_name_returns_inactive(self):
        factory = RequestFactory()
        request = factory.get("/")
        t = Template("{% load core_tags %}{% active_nav 'nonexistent_url_name_xyz' %}")
        out = t.render(Context({"request": request}))
        assert "text-gray-600" in out

    @pytest.mark.django_db
    def test_active_on_prefix_match(self):
        factory = RequestFactory()
        request = factory.get("/services/etudes-techniques/")
        t = Template("{% load core_tags %}{% active_nav 'services' %}")
        out = t.render(Context({"request": request}))
        assert "text-primary-700" in out
