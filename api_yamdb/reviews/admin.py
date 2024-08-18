from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, Review, Title, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


class TitleAdmin(admin.ModelAdmin):
    list_display = ["name", "year", "description", "category"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "text",
        "author",
        "pub_date",
        "score",
        "title",
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["text", "author", "pub_date", "review"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
