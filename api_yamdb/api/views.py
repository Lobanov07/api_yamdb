from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ('get', 'patch', 'post', 'delete')
