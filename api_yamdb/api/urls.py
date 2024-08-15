from django.urls import include, path
from rest_framework import routers

from .views import (UserViewSet,
                    APISignup, APIGetToken)

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='get_token')


auth = [
    path('signup/', APISignup.as_view(), name='register'),
    path('token/', APIGetToken.as_view(), name='token')
]


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth)),
]
