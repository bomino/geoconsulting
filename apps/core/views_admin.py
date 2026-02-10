from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse


@staff_member_required
def admin_guide_view(request):
    context = {**admin.site.each_context(request), "title": "Guide d'administration"}
    return TemplateResponse(request, "admin/guide.html", context)
