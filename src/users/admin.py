from django.contrib import admin
from django.contrib.auth import get_user_model

from issues.models import Issue

User = get_user_model()


class IssuesInline(admin.TabularInline):
    model = Issue
    readonly_fields = ("status", "body", "title")
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("email", "first_name", "last_name")
    inlines = [
        IssuesInline,
    ]

    exclude = ["user_permissions", "groups"]
    readonly_fields = [
        "password",
        "date_joined",
        "last_login",
        "is_superuser",
        "email",
    ]
