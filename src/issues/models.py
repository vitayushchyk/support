from enum import IntEnum

from django.db import models

from users.models import User


class Status(IntEnum):
    OPENED = 1
    IN_PROGRESS = 2
    CLOSED = 3


ISSUE_STATUS_CHOICES = (
    (1, "Opened"),
    (2, "In progress"),
    (3, "Closed"),
)


class Issue(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    status = models.PositiveIntegerField(
        null=True, default=Status.OPENED, choices=ISSUE_STATUS_CHOICES
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="issues",
        default=None,
    )

    def __repr__(self) -> str:
        return f"Issue[{self.pk} {self.title[:10]}]"


class Message(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    # update on any update in the colum
    #  updated = models.DateTimeField(auto_now=True)
