from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from .mixins import UsernameMixin
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
