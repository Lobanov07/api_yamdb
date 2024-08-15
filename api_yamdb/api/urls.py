from django.urls import include, path
from rest_framework import routers

from .views import (UserViewSet,
                    APISignup, APIGetToken)

router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='get_token')


auth = [
    path('signup/', APISignup.as_view(), name='register'),
    path('token/', APIGetToken.as_view(), name='token')
]


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth)),
]
