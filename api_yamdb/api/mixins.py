from reviews.validators import user_name


class UsernameMixin:
    def validate_username(self, username):
        return user_name(username)
