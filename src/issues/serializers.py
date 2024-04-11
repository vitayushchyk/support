from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from issues.models import Issue


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
        )
        issue.save()
        return issue


class IssueRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "body", "creator"]
        permission_classes = (IsAuthenticated,)
