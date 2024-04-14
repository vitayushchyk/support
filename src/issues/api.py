from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from issues.models import Issue
from issues.serializers import (
    IssueCreateSerializer,
    IssueRetrieveUpdateDestroySerializer,
)


class IssueCreateAPIView(CreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueCreateSerializer
    permission_classes = (IsAuthenticated,)


class IssueRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueRetrieveUpdateDestroySerializer
    permission_classes = (IsAuthenticated,)
