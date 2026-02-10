from apps.contacts.models import ContactAssignment
from apps.crm.models import AssignmentRule


def auto_assign_contact(contact):
    rules = AssignmentRule.objects.filter(active=True).order_by("-priority")
    text = f"{contact.subject} {contact.message}".lower()
    for rule in rules:
        keywords = [k.strip().lower() for k in rule.keywords if isinstance(k, str) and k.strip()]
        if any(kw in text for kw in keywords):
            ContactAssignment.objects.create(
                contact=contact,
                assigned_to=rule.assigned_user,
                rule=rule,
            )
            return True
    return False
