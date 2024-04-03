from django.db import models

from users.models import User


class Issue(models.Model):
    title = models.CharField(max_length=100)
    status = models.PositiveIntegerField()
    junior = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="junior_issues",
        default=None,
    )
    senior = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="senior_issues",
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
