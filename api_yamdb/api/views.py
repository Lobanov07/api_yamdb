import random

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import (
    IsAdmin,
    IsOwnerAdminModeratorOrReadOnly,
    IsAdminOrReadOnly
)
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    NotAdminSerializer,
    GetTokenSerializer,
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
    User
)

# User = get_user_model()


class ListCreateDelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class UserViewSet(viewsets.ModelViewSet):
    """Класс вьюсет для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'patch', 'post', 'delete')

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path=settings.MY_PAGE)
    def get_patch_current_user_info(self, request):
        if request.method == 'GET':
            return Response(
                UserSerializer(request.user).data,
                status=status.HTTP_200_OK
            )
        serializer = NotAdminSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        user.confirmation_code = settings.DEFAULT_CONF_CODE
        user.save()
        raise ValidationError('Неверно! запросите новый код подтверждения')


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data)

        except IntegrityError:
            raise ValidationError(
                'Пользователь {} уже зарегистрирован.'.format(
                    'email' if User.objects.filter(email=email) else 'именем')
            )

        user.confirmation_code = ''.join(random.sample(
            settings.PATTERN, settings.CODE_MAX_LEN
        ))
        user.save()

        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {user.confirmation_code}',
            from_email=settings.DEFAULT_EMAIL,
            recipient_list=[email],
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'patch', 'post', 'delete')

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
