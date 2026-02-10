import factory
from django.utils.text import slugify

from apps.accounts.factories import UserFactory
from apps.articles.models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Sequence(lambda n: f"Article test {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    content = "Contenu de l'article de test."
    category = "Entreprise"
    published = False
    created_by = factory.SubFactory(UserFactory)
