from django.contrib import admin
from django.urls import path

from issues.api import create_issue, get_issues

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", get_issues),
    path("issues/create", create_issue),
]
