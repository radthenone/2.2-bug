import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.required = tuple(re.compile(url) for url in settings.UNAVAILABLE_URLS)
        self.exceptions = tuple(re.compile(url) for url in settings.AVAILABLE_URLS)

    def __call__(self, request):
        response = self.process_view(request)

        if response is None:
            response = self.get_response(request)

        return response

    def process_view(self, request, view_func=None, view_args=None, view_kwargs=None):
        if request.user.is_authenticated:
            for url in self.exceptions:
                if url.match(request.path):
                    return redirect("home")

            return None

        for url in self.required:
            if url.match(request.path):
                if view_func is not None:
                    return login_required(view_func)(
                        request, *view_args or [], **view_kwargs or {}
                    )
                else:
                    return redirect("auth:login")

        return None
