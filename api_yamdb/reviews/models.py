# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

from reviews.validators import real_age, validate_score, user_name
from api_yamdb.settings import MAXLENGTH, LENGTHTEXT

# User = get_user_model()


class User(AbstractUser):
    '''User класс '''
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        'Логин',
        max_length=150,  # вынесу - когда решим как хроним константы
        unique=True,
        validators=(user_name,),
    )
    email = models.EmailField(
        'E-mail',
        unique=True,
        # validators=(),
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,  # !
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,  # !
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        null=True,
        blank=True,
    )

    role = models.CharField(
        'Роль',
        max_length=150,  # !
        default=USER,
        choices=ROLES,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=5,  # !
        default=5,  # !
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:20]  # !


class Categories(models.Model):
    """Модель Categories."""

    name = models.CharField(
        max_length=MAXLENGTH,
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
        max_length=MAXLENGTH,
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
        max_length=MAXLENGTH,
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
        return self.name[:LENGTHTEXT]


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
        return self.title[:LENGTHTEXT]


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
        return self.text[:LENGTHTEXT]
