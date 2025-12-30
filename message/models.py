from django.db import models

# Create your models here.
from django.db import models

class MessageThread(models.Model):
    user1 = models.ForeignKey("accounts.User", related_name="thread_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey("accounts.User", related_name="thread_user2", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"Thread: {self.user1} & {self.user2}"

class Message(models.Model):
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

