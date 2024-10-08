from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
    APISignup,
    APIGetToken,
)

router = routers.DefaultRouter()
router.register(
    "categories",
    CategoryViewSet,
    basename="categories"
)
router.register(
    "genres",
    GenreViewSet,
    basename="genres"
)
router.register(
    "titles",
    TitleViewSet,
    basename="titles"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register("users", UserViewSet)


auth = [
    path("signup/", APISignup.as_view(), name="register"),
    path("token/", APIGetToken.as_view(), name="token"),
]


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(auth)),
]
