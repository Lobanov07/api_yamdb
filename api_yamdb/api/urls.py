from django.urls import include, path
from rest_framework import routers

from api.views import (
    UserViewSet,
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
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


urlpatterns = [
    path('v1/', include(router.urls)),
]
