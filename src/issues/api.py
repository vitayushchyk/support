from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "body", "junior_id", "senior_id"]


@api_view()
def get_issues(request) -> Response:
    issues = Issue.objects.all()
    results = [IssueSerializer(issue).data for issue in issues]

    return Response(data={"results": results})


@api_view(["POST"])
def create_issue(request) -> Response:
    serializer = IssueSerializer(data=request.data)
    if serializer.is_valid():
        issue = serializer
        issue.save()
        return Response(issue.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
