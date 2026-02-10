import pytest

from apps.crm.factories import AssignmentRuleFactory
from apps.crm.models import AssignmentRule


@pytest.mark.django_db
class TestAssignmentRule:
    def test_ordering_by_priority_desc(self):
        r1 = AssignmentRuleFactory(priority=5)
        r2 = AssignmentRuleFactory(priority=10)
        result = list(AssignmentRule.objects.all())
        assert result[0] == r2

    def test_keywords_json_roundtrip(self):
        keywords = ["route", "pont", "hydraulique"]
        rule = AssignmentRuleFactory(keywords=keywords)
        rule.refresh_from_db()
        assert rule.keywords == keywords
