import factory

from apps.accounts.factories import UserFactory
from apps.core.enums import TemplateCategory
from apps.crm.models import AssignmentRule, EmailTemplate


class EmailTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailTemplate

    name = factory.Sequence(lambda n: f"Template {n}")
    subject = "Sujet du template"
    body = "Corps du template de test."
    category = TemplateCategory.CUSTOM
    created_by = factory.SubFactory(UserFactory)


class AssignmentRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignmentRule

    name = factory.Sequence(lambda n: f"Regle {n}")
    keywords = ["test", "devis"]
    assigned_user = factory.SubFactory(UserFactory)
    priority = 0
    active = True
    created_by = factory.SubFactory(UserFactory)
