from django.urls import path

from app.apps.posts.views import (
    PostCreateView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("new/", PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
]
