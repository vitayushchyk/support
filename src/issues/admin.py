from django.contrib import admin

from issues.models import Issue, Message


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "creator")
    list_filter = ("status",)


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ("id", "body", "issue", "timestamp")
