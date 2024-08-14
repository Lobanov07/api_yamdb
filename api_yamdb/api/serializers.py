import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from api.mixins import UsernameMixin
from reviews.models import Categories, Genres, Title, Review, Comments


class ReviewSerializer(serializers.ModelSerializer, UsernameMixin):
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
    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('id', 'review')
