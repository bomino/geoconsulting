from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def client_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.groups.filter(name="clients").exists()):
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper
