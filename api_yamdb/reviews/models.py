from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

from reviews.validators import (
    real_age,
    validate_score,
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


class Categories(models.Model):
    """Модель Categories."""

    name = models.CharField(
        max_length=settings.MAXLENGTH,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'

    def __str__(self):
        return self.name


class Genres(models.Model):
    """Модель Genres."""

    name = models.CharField(
        max_length=settings.MAXLENGTH,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг жанра содержит недопустимый символ'
        )]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель Title."""

    name = models.CharField(
        max_length=settings.MAXLENGTH,
        verbose_name='Произведение'
    )
    year = models.IntegerField(
        validators=(real_age,),
        verbose_name='Год создания'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='категория'
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        ordering = ('-year', 'name')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return self.name[:settings.LENGTHTEXT]


class Review(models.Model):
    """Модель Review."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True
    )
    text = models.TextField(
        verbose_name='текст'
    )
    score = models.PositiveSmallIntegerField(
        validators=(validate_score,),
        verbose_name='рейтинг', 
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_title'
            ),
        ]
        ordering = ('-pub_date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.title[:settings.LENGTHTEXT]


class Comments(models.Model):
    """Модель Comments."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор',
        null=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='oтзыв'
    )
    text = models.TextField(
        verbose_name='текст'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.LENGTHTEXT]
