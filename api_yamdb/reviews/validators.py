import datetime
import re

from django.conf import settings
from django.core.exceptions import ValidationError


def real_age(value):
    if value > datetime.datetime.now().year and value < 0:
        raise ValidationError(
            'Вы ввели некорректный год.'
            'Год создания произведения не может быть больше текущего'
            'и меньше начала нашей эры.'
        )

def validate_score(value):
    if value < 1 or value > 10:
        raise ValidationError(
            f'Значение должно быть в диапазоне от 1 до 10. Указано: {value}'
        )

def validate_score(value):
    if value < 1 or value > 10:
        raise ValidationError(
            f'Значение должно быть в диапазоне от 1 до 10. Указано: {value}'
        )


def user_name(username):
    forbidden_chars = re.findall(r'[^\w.@+-]', username)
    if forbidden_chars:
        raise ValidationError(
            f'Недопустимые символы: {set(forbidden_chars)}'
        )
    return username


def username_is_not_forbidden(value):
    if value in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Имя пользователя {value} не разрешено.'
        )
    return value


def validate_confirmation_code(pin_code):
    invalid_chars = re.findall(
        fr'{re.escape(settings.PATTERN)}', pin_code
    )
    if invalid_chars:
        raise ValidationError(
            f'Код не должен содержать символы {set(invalid_chars)}'
        )
    return pin_code
