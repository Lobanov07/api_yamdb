import datetime
import re

# from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from .mixins import UsernameMixin
from reviews.validators import validate_confirmation_code
from reviews.models import (
    Categories,
    Genres,
    Title,
    Review,
    Comments,
    User
)

# User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class GetTokenSerializer(serializers.Serializer, UsernameMixin):
    username = serializers.CharField(required=True,
                                     max_length=settings.USER_MAX_LENGTH)
    confirmation_code = serializers.CharField(
        required=True,
        max_length=settings.CODE_MAX_LEN,
        validators=(validate_confirmation_code,)
    )

    def validate_confirmation_code(self, pin_code):
        if pin_code == settings.DEFAULT_CONF_CODE:
            raise ValidationError(
                'Ошибка. Сначала получите код подтверждения.'
            )
        invalid_chars = re.findall(
            fr"'{re.escape(settings.PATTERN)}\s'", pin_code
        )
        if invalid_chars:
            raise ValidationError(
                f'Код не должен содержать символы {invalid_chars}'
            )
        return pin_code


class SignUpSerializer(serializers.Serializer, UsernameMixin):
    username = serializers.CharField(required=True,
                                     max_length=settings.USER_MAX_LENGTH)
    email = serializers.EmailField(required=True,
                                   max_length=settings.MAX_LENGTH_EMAIL)


class NotAdminSerializer(serializers.ModelSerializer, UsernameMixin):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer, UsernameMixin):
    """Класс сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        if Review.objects.filter(
                title=get_object_or_404(
                    Title, pk=self.context['view'].kwargs.get('title_id')
                ), author=request.user
        ).exists():
            raise ValidationError('Вы не можете добавить более'
                                  'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CategoriesSerializer(serializers.ModelSerializer):
    """Класс сериализатор для модели Categories."""
    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    """Класс сериализатор для модели Genres."""
    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Класс сериализатор для модели Title."""
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category', 'rating'
        )


class CreateTitleSerializer(serializers.ModelSerializer):
    """Класс сериализатор для создания объектов модели Title."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        if value > datetime.datetime.now().year and value < 0:
            raise ValidationError(
                'Вы ввели некорректный год.'
                'Год создания произведения не может быть больше текущего'
                'и меньше начала нашей эры.'
            )
        return value


class CommentsSerializer(serializers.ModelSerializer):
    """Класс сериализатор для создания объектов модели Comments."""
    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'review')
