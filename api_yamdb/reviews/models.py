from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from reviews.validators import (
    username_is_not_forbidden,
    user_name
)


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        max_length=settings.USER_MAX_LENGTH,
        unique=True,
        validators=(
            user_name,
            username_is_not_forbidden,
        ),
        verbose_name='имя пользователя',
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='биография'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='email адрес'
    )
    role = models.CharField(
        default=USER,
        choices=ROLES,
        max_length=max(len(role) for role, _ in ROLES),
        verbose_name='роль'
    )
    first_name = models.CharField(
        max_length=settings.USER_MAX_LENGTH,
        blank=True,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=settings.USER_MAX_LENGTH,
        blank=True,
        verbose_name='фамилия'
    )
    confirmation_code = models.CharField(
        max_length=settings.CODE_MAX_LEN,
        default=settings.CODE_MAX_LEN,
        verbose_name='код подтверждения'
    )

    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=["email", "username"],
                name="unique_email_username",
            ),
        ]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    def __str__(self):
        return self.username[:settings.ADMIN_DISPLEY_PAGINATOR]
