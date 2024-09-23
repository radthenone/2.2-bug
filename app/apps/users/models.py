from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from app.apps.users.manager import UserManager

# Create your models here.


class UserModel(AbstractBaseUser):
    email = models.EmailField("email", unique=True)
    username = models.CharField("username", max_length=30, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
