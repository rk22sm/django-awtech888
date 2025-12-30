from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Profile,User, NotificationSettings

User = settings.AUTH_USER_MODEL



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_related_models(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        NotificationSettings.objects.create(user=instance)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.id}",  # ✅ instance is the User
            {
                "type": "notify",
                "message": "Welcome! Your profile is ready.",
            }
        )

@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        NotificationSettings.objects.get_or_create(user=instance)