from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues.models import Issue
from issues.serializers import (
    IssueCreateSerializer,
    IssueRetrieveUpdateDestroySerializer,
)
from users.models import Role


class IssueCreateAPIView(CreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueCreateSerializer
    permission_classes = (IsAuthenticated,)


class IssueRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueRetrieveUpdateDestroySerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        if request.user.role != Role.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.role not in (Role.ADMIN, Role.SENIOR):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().put(request, *args, **kwargs)


class IssueListAPIView(ListAPIView):
    serializer_class = IssueRetrieveUpdateDestroySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        role = user.role

        if role == Role.ADMIN:
            return Issue.objects.all()
        elif role == Role.SENIOR:
            return Issue.objects.filter(creator=user)
        elif role == Role.JUNIOR:
            return Issue.objects.filter(creator=user)
        else:
            return Issue.objects.none()
