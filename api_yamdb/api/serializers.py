import re

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .mixins import UsernameMixin
from reviews.validators import validate_confirmation_code

User = get_user_model()

MAX_LENGTH_USERNAME = 150
MAX_LENGTH_EMAIL = 254


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class GetTokenSerializer(serializers.Serializer, UsernameMixin):
    username = serializers.CharField(required=True,
                                     max_length=MAX_LENGTH_USERNAME)
    confirmation_code = serializers.CharField(
        required=True,
        max_length=settings.CODE_MAX_LEN,
        validators=(validate_confirmation_code,)
    )

    def validate_confirmation_code(self, pin_code):
        if pin_code == settings.DEFAULT_CONF_CODE:
            raise ValidationError(
                'Ошибка. Сначала получите код подтверждения.'
            )
        invalid_chars = re.findall(
            fr"'{re.escape(settings.PATTERN)}\s'", pin_code
        )
        if invalid_chars:
            raise ValidationError(
                f'Код не должен содержать символы {invalid_chars}'
            )
        return pin_code


class SignUpSerializer(serializers.Serializer, UsernameMixin):
    username = serializers.CharField(required=True,
                                     max_length=MAX_LENGTH_USERNAME)
    email = serializers.EmailField(required=True,
                                   max_length=MAX_LENGTH_EMAIL)


class NotAdminSerializer(serializers.ModelSerializer, UsernameMixin):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
