from django.urls import include, path
from rest_framework import routers

from api.views import (
    UserViewSet,
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

app_name = 'api'


router = routers.DefaultRouter()
router.register('users', UserViewSet,)

router.register(
    'categories',
    CategoriesViewSet,
    basename='categories'
)

router.register(
    'genres',
    GenresViewSet,
    basename='genres'
)

router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
