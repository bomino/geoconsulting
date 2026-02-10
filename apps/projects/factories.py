import factory
from django.utils.text import slugify

from apps.accounts.factories import UserFactory
from apps.core.enums import ProjectCategory
from apps.projects.models import Project, ProjectDocument


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Sequence(lambda n: f"Projet test {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    description = "Description du projet de test."
    category = ProjectCategory.ROUTES
    published = True
    created_by = factory.SubFactory(UserFactory)


class ProjectDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectDocument

    project = factory.SubFactory(ProjectFactory)
    title = factory.Sequence(lambda n: f"Document {n}")
    file = factory.django.FileField(filename="rapport.pdf")
    uploaded_by = factory.SubFactory(UserFactory)
