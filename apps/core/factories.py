import factory

from apps.accounts.factories import UserFactory
from apps.core.enums import Department
from apps.core.models import FAQ, FAQCategory, SiteSetting, TeamMember


class FAQFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FAQ

    question = factory.Sequence(lambda n: f"Question {n}?")
    answer = "Reponse de test."
    category = FAQCategory.GENERAL
    order = factory.Sequence(lambda n: n)
    published = True
    created_by = factory.SubFactory(UserFactory)


class TeamMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TeamMember

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = "Ingenieur"
    department = Department.ETUDES
    order = factory.Sequence(lambda n: n)
    published = True


class SiteSettingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SiteSetting

    key = factory.Sequence(lambda n: f"setting_{n}")
    value = "test value"
