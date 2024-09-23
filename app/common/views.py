from app.apps.posts.models import PostModel
from django.db.models import Q
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context["posts"] = PostModel.objects.filter(
                Q(status="published") | Q(author=user)
            ).distinct()
        else:
            context["posts"] = PostModel.objects.filter(status="published")
        return context
