from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class PostModel(models.Model):
    author = models.ForeignKey("custom_users.UserModel", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        default="draft",
        choices=[("draft", "Draft"), ("published", "Published")],
    )

    objects = models.Manager()

    def publish(self):
        self.published_date = timezone.now()
        self.status = "published"
        self.save()

    def edit(self):
        self.updated_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"pk": self.pk})

    def get_created_date(self):
        return self.created_date.strftime("%Y-%m-%d")  # noqa

    class Meta:
        db_table = "posts"
        ordering = ["-published_date"]

    def __str__(self):
        return self.title
