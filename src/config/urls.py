from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from issues.api import IssueCreateAPIView, IssueRetrieveUpdateDestroyAPIView
from users.appi import UserCreateAPIView, UserRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", IssueCreateAPIView.as_view(), name="issue-create"),
    path("issues/<int:pk>", IssueRetrieveUpdateDestroyAPIView.as_view(), name="issues"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/", UserCreateAPIView.as_view(), name="user-create"),
    path(
        "user/<int:pk>",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-retrieve-update-destroy",
    ),
]
