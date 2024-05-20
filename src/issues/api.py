from django.db.models import Q
from rest_framework import response, status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from issues.models import Issue, Message, Status
from issues.serializers import (
    IssueCreateSerializer,
    IssueRetrieveUpdateDestroySerializer,
    MessageSerializer,
)
from users.models import Role


class IsSenior(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == Role.SENIOR)


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


class MessageListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get(self, request: Request, issue_id: int):
        messages = Message.objects.filter(
            Q(issue__id=issue_id) & Q(user=request.user)
        ).order_by("-timestamp")
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)

    def post(self, request: Request, issue_id: int):
        issue = Issue.objects.get(id=issue_id)
        payload = request.data | {"issue": issue.id} | {"user": request.user.id}
        serializer = self.serializer_class(data=payload, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)


class IssueCloseUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSenior)
    serializer_class = IssueRetrieveUpdateDestroySerializer

    def put(self, request: Request, pk: int):
        issue = Issue.objects.get(pk=pk)

        if issue.status != Status.IN_PROGRESS:
            return Response(
                {"message": "Issue must be in 'IN_PROGRESS' state to be closed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        issue.assigning_to = request.user
        issue.senior = request.user
        issue.status = Status.CLOSED
        issue.save()

        serializer = self.serializer_class(issue)
        return response.Response(serializer.data)


class IssueTakeUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSenior)
    serializer_class = IssueCreateSerializer

    def put(self, request: Request, pk: int):
        issue = Issue.objects.get(pk=pk)

        if (issue.status != Status.OPENED) or (issue.creator.role is None):
            return response.Response(
                {"message": "Issue is not Opened or senior is set..."},
                status=422,
            )

        issue.assigning_to = request.user
        issue.senior = request.user
        issue.status = Status.IN_PROGRESS
        issue.save()
        serializer = self.serializer_class(issue)
        return response.Response(serializer.data)
