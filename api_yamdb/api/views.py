from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .permissions import IsOwnerAdminModeratorOrReadOnly
from .serializers import ReviewSerializer
from reviews.models import Categories, Genres, Title, Review, Comments

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ('get', 'patch', 'post', 'delete')


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)
    http_method_names = ('get', 'patch', 'post', 'delete')
    serializer_class = ReviewSerializer

    def get_tile(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_tile().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_tile())
