from django.db.models import Q
from rest_framework import response, serializers, status
from rest_framework.decorators import api_view
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from issues.models import Issue, Message, Status
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


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Message
        fields = "__all__"

    def save(self):
        if (user := self.validated_data.pop("user", None)) is not None:
            self.validated_data["user_id"] = user.id

        if (issue := self.validated_data.pop("issue", None)) is not None:
            self.validated_data["issue_id"] = issue.id

        return super().save()


@api_view(["GET", "POST"])
def messages_api_dispatcher(request: Request, issue_id: int):
    if request.method == "GET":
        messages = Message.objects.filter(
            Q(
                issue__id=issue_id,
            )
            & (
                Q(
                    user=request.user,
                )
            )
        ).order_by("-timestamp")
        serializer = MessageSerializer(messages, many=True)

        return response.Response(serializer.data)
    else:
        issue = Issue.objects.get(id=issue_id)
        payload = request.data | {"issue": issue.id} | {"user": request.user.id}
        serializer = MessageSerializer(data=payload, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.validated_data)


@api_view(["PUT"])
def issues_close(request: Request, pk: int):
    issue = Issue.objects.get(pk=pk)

    if request.user.role != Role.SENIOR:
        raise PermissionError("Only senior users can take issues")

    if issue.status != Status.IN_PROGRESS:
        return Response(
            {"message": "Issue must be in 'IN_PROGRESS' state to be closed."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    issue.assigning_to = request.user
    issue.senior = request.user
    issue.status = Status.CLOSED
    issue.save()

    serializer = IssueRetrieveUpdateDestroySerializer(issue)
    return response.Response(serializer.data)


@api_view(["PUT"])
def issues_take(request: Request, pk: int):
    issue = Issue.objects.get(id=pk)

    if request.user.role != Role.SENIOR:
        raise PermissionError("Only senior users can take issues")

    if (issue.status != Status.OPENED) or (issue.creator.role is None):

        return response.Response(
            {"message": "Issue is not Opened or senior is set..."},
            status=422,
        )
    else:
        issue.assigning_to = request.user
        issue.senior = request.user
        issue.status = Status.IN_PROGRESS
        issue.save()

    serializer = IssueCreateSerializer(issue)
    return response.Response(serializer.data)
