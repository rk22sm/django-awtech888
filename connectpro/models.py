from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Connection(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"

    from_user = models.ForeignKey(
        User, related_name="sent_connections", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="received_connections", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")
