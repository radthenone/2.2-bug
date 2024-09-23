from django.shortcuts import redirect


class RedirectAuthenticatedUserMixin:
    success_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
