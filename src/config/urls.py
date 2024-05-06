from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView

from issues.api import (
    IssueCreateAPIView,
    IssueListAPIView,
    IssueRetrieveUpdateDestroyAPIView,
    issues_close,
    issues_take,
    messages_api_dispatcher,
)
from users.appi import UserCreateAPIView, UserRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    # ADMIN
    path("admin/", admin.site.urls),
    # ISSUES
    path("issues/query/", IssueListAPIView.as_view(), name="issue-get_queryset"),
    path("issues/create/", IssueCreateAPIView.as_view(), name="issue-create"),
    path(
        "issues/<int:pk>",
        IssueRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path("issues/<int:pk>/close", issues_close),
    path("issues/<int:pk>/take", issues_take),
    # MESSAGES
    path("issues/<int:issue_id>/messages", messages_api_dispatcher),
    # TOKEN
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # USER
    path("user/", UserCreateAPIView.as_view(), name="user-create"),
    path(
        "user/<int:pk>",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-retrieve-update-destroy",
    ),
]
