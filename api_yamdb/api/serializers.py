import re

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from .mixins import UsernameMixin
from reviews.validators import validate_confirmation_code
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class GetTokenSerializer(serializers.Serializer, UsernameMixin):
    username = serializers.CharField(required=True, max_length=settings.USER_MAX_LENGTH)
    confirmation_code = serializers.CharField(
        required=True,
        max_length=settings.CODE_MAX_LEN,
        validators=(validate_confirmation_code,),
    )

    def validate_confirmation_code(self, pin_code):
        if pin_code == settings.DEFAULT_CONF_CODE:
            raise ValidationError("Ошибка. Сначала получите код подтверждения.")
        invalid_chars = re.findall(rf"'{re.escape(settings.PATTERN)}\s'", pin_code)
        if invalid_chars:
            raise ValidationError(f"Код не должен содержать символы {invalid_chars}")
        return pin_code


class SignUpSerializer(serializers.Serializer, UsernameMixin):
    username = serializers.CharField(required=True, max_length=settings.USER_MAX_LENGTH)
    email = serializers.EmailField(required=True, max_length=settings.MAX_LENGTH_EMAIL)


class NotAdminSerializer(serializers.ModelSerializer, UsernameMixin):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class ReviewSerializer(serializers.ModelSerializer, UsernameMixin):
    """Класс сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(), slug_field="username", read_only=True
    )

    def validate(self, data):
        request = self.context["request"]
        if request.method != "POST":
            return data
        if Review.objects.filter(
            title=get_object_or_404(
                Title, pk=self.context["view"].kwargs.get("title_id")
            ),
            author=request.user,
        ).exists():
            raise ValidationError(
                "Вы не можете добавить более" "одного отзыва на произведение"
            )
        return data

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CategorySerializer(serializers.ModelSerializer):
    """Класс сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    """Класс сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"


class TitleSerializer(serializers.ModelSerializer):
    """Класс сериализатор для модели Title."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category", "rating")


class CreateTitleSerializer(serializers.ModelSerializer):
    """Класс сериализатор для создания объектов модели Title."""

    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")


class CommentSerializer(serializers.ModelSerializer):
    """Класс сериализатор для создания объектов модели Comment."""

    author = SlugRelatedField(
        slug_field="username", default=serializers.CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("id", "review")
