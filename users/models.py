from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import CustomUserManager


class User(AbstractUser):
    """AbstractUser class
    used for customising default django User model
    """

    username = None  # type: ignore
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    objects = CustomUserManager()  # type: ignore #https://github.com/typeddjango/django-stubs/issues/174
