from django.urls import path

from apps.projects.views import ProjectDetailView, ProjectListView

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("<slug:slug>/", ProjectDetailView.as_view(), name="project_detail"),
]
