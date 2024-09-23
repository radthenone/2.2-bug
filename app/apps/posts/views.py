from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from app.apps.posts.forms import PostForm
from app.apps.posts.models import PostModel

# Create your views here.


class PostCreateView(CreateView):
    model = PostModel
    form_class = PostForm
    template_name = "posts/post.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = PostModel
    form_class = PostForm
    template_name = "posts/post.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return PostModel.objects.filter(author=self.request.user)

    def form_valid(self, form):
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect("home")


class PostDetailView(DetailView):
    model = PostModel
    form_class = PostForm
    template_name = "posts/post-detail.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "pk"

    def get_object(self, queryset=None):
        return get_object_or_404(PostModel, pk=self.kwargs[self.pk_url_kwarg])

    def post(self, request, *args, **kwargs):
        post_model = self.get_object()
        if "publish" in request.POST:
            post_model.publish()
            return redirect("home")
        elif "edit" in request.POST:
            return redirect("post:post_edit", pk=post_model.pk)
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect("base")


class PostListView(ListView):
    model = PostModel
    template_name = "posts/post-list.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return PostModel.objects.filter(
                Q(status="published") | Q(author=user)
            ).distinct()
        else:
            return PostModel.objects.filter(status="published")
