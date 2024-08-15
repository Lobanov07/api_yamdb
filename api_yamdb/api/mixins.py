from reviews.validators import user_name, username_is_not_forbidden


class UsernameMixin:
    def validate_username(self, username):
        return user_name(username_is_not_forbidden(username))
