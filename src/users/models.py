import uuid
from enum import IntEnum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class Role(IntEnum):
    ADMIN = 1
    SENIOR = 2
    JUNIOR = 3


Role_CHOICES = (
    (1, "Admin"),
    (2, "Senior"),
    (3, "Junior"),
)


class User(AbstractUser):
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(max_length=128, unique=True, blank=False, null=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    role = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        default=Role.JUNIOR,
        choices=Role_CHOICES,
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """

        return f"{self.get_role_name()}: {self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""

        return self.first_name

    def get_role_name(self):
        return {
            Role.ADMIN: "Administrator",
            Role.SENIOR: "Senior",
            Role.JUNIOR: "Junior",
        }[Role(self.role)]

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.email


class ActivationKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(
        max_length=100, unique=True, default=uuid.uuid4, editable=False
    )

    def __str__(self):
        return f"Activation Key for {self.user.username}"
