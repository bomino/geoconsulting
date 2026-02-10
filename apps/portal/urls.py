from django.urls import path

from apps.portal.views import (
    DocumentDownloadView,
    MarkAsReadView,
    MessageComposeView,
    MessageDetailView,
    MessageListView,
    PortalDashboardView,
    PortalProjectView,
)

urlpatterns = [
    path("", PortalDashboardView.as_view(), name="portal_dashboard"),
    path("projets/<slug:slug>/", PortalProjectView.as_view(), name="portal_project"),
    path(
        "projets/<slug:slug>/telecharger/<int:doc_id>/",
        DocumentDownloadView.as_view(),
        name="portal_document_download",
    ),
    path("messages/", MessageListView.as_view(), name="portal_messages"),
    path("messages/nouveau/", MessageComposeView.as_view(), name="portal_message_compose"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="portal_message_detail"),
    path("messages/<int:pk>/lu/", MarkAsReadView.as_view(), name="portal_mark_read"),
]
