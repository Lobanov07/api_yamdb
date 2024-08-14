from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import viewsets, filters, mixins

from api.permissions import IsOwnerAdminModeratorOrReadOnly
from api.serializers import (
    ReviewSerializer,
    CategoriesSerializer,
    GenresSerializer,
    TitleSerializer,
    CreateTitleSerializer,
    CommentsSerializer
)
from api.filters import TitleFilter
from reviews.models import (
    Categories,
    Genres,
    Title,
    Review,
    Comments
)

User = get_user_model()


class ListCreateDelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class UserViewSet(viewsets.ModelViewSet):
    """Класс вьюсет для модели User."""
    queryset = User.objects.all()
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ('get', 'patch', 'post', 'delete')


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс вьюсет для модели Review."""
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)
    http_method_names = ('get', 'patch', 'post', 'delete')
    serializer_class = ReviewSerializer

    def get_tile(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_tile().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_tile())


class CategoriesViewSet(ListCreateDelViewSet):
    """Класс вьюсет для модели Categories."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(ListCreateDelViewSet):
    """Класс вьюсет для модели Genre."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Класс вьюсет для модели Title."""

    queryset = Title.objects.select_related('category').\
        prefetch_related('genre').annotate(rating=Avg('reviews__score'))
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return CreateTitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Класс вьюсет для модели Comments."""
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)
    http_method_names = ('get', 'patch', 'post', 'delete')
    serializer_class = CommentsSerializer

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
