from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint

from reviews.validators import real_age

User = get_user_model()


class User():
    ...


class Categories(models.Model):
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
    name = models.CharField(
        max_length=settings.MAXLENGTH,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный идентификатор'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
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
        verbose_name='описание'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        max_length=settings.MAXLENGTH,
        blank=True,
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
        ordering = ('year',)
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['title', 'author'], name='unique_following'
            ),
        ]
        ordering = ('pub_date',)
        verbose_name = 'отзыв'

    def __str__(self):
        return self.title


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'комментарий'

    def __str__(self):
        return self.review
