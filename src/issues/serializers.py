from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from issues.models import Issue, Message


class IssueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "body"]
        permission_classes = (IsAuthenticated,)

    def create(self, validated_data):
        issue = Issue.objects.create(
            title=validated_data["title"],
            body=validated_data["body"],
            creator=self.context.get("request").user,
            assigning_to=None,
        )

        issue.save()
        return issue


class IssueRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "body", "creator"]
        permission_classes = (IsAuthenticated,)


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
