from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from accounts.models import User, Notification,NotificationSettings
from .models import MessageThread, Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import Notification
from django.utils.timezone import now
from django.http import JsonResponse



@login_required
def inbox(request):
    thread_id = request.GET.get("thread")
    active_thread = None
    other_user = None
    messages_payload = []

    # Get all threads for sidebar
    threads = MessageThread.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).order_by("-created_at")

    thread_details = []
    for t in threads:
        other = t.user1 if t.user2 == request.user else t.user2
        last = t.message_set.order_by("-timestamp").first()
        thread_details.append({
            "thread": t,
            "other": other,
            "last_message": last
        })

    if thread_id:
        try:
            active_thread = MessageThread.objects.get(
                Q(user1=request.user) | Q(user2=request.user),
                id=thread_id
            )
        except MessageThread.DoesNotExist:
            active_thread = None

        if active_thread:
            other_user = active_thread.user1 if active_thread.user2 == request.user else active_thread.user2

            # Fetch messages
            messages = Message.objects.filter(thread=active_thread).order_by("timestamp")
            messages_payload = [
                {
                    "id": m.id,
                    "content": m.content,
                    "sender": m.sender.username,
                    "is_me": m.sender == request.user,
                    "timestamp": m.timestamp.isoformat()
                } for m in messages
            ]

            # ✅ Mark all notifications related to this thread as read
            Notification.objects.filter(
            user=request.user,
            is_read=False,
            thread=active_thread
            ).update(is_read=True)


    # Prepare notifications for dropdown
    unread_notifications_qs = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    unread_count = unread_notifications_qs.count()
    unread_notifications = list(unread_notifications_qs.values('actor__username', 'verb', 'target', 'created_at'))

    notifications_qs = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications = list(notifications_qs.values('actor__username', 'verb', 'target', 'created_at'))

    return render(request, "messages/inbox.html", {
        "thread_details": thread_details,
        "active_thread": active_thread,
        "other_user": other_user,
        "messages_payload": messages_payload,
        "notifications": notifications,
        "notifications_unread_count": unread_count,
        "unread_notifications": unread_notifications,
    })


@login_required
def send_message(request, thread_id):
    thread = get_object_or_404(MessageThread, id=thread_id)

    if request.method == "POST":
        content = request.POST.get("message")

        # Create the message
        msg = Message.objects.create(
            thread=thread,
            sender=request.user,
            content=content
        )

        # Determine receiver
        receiver = thread.user1 if thread.user2 == request.user else thread.user2

        # Ensure NotificationSettings exists
        settings, _ = NotificationSettings.objects.get_or_create(user=receiver)

        # Send DB notification if enabled
        if settings.message_notifications:
            Notification.objects.create(
                user=receiver,
                actor=request.user,
                verb="",
                target=content[:30],
                thread = thread,
            )

            # 🔔 Send real-time notification via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{receiver.id}",
                {
                    "type": "notify",
                    "actor": request.user.username,
                    "verb": "sent you a message",
                    "created_at": now().strftime("%H:%M"),
                }
            )

    return redirect(f"/messages/?thread={thread.id}")

@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    user1, user2 = sorted([request.user, other_user], key=lambda u: u.id)

    thread, created = MessageThread.objects.get_or_create(
        user1=user1,
        user2=user2
    )
   
    return redirect(f"/messages/?thread={thread.id}")

@login_required
@require_POST
def mark_thread_notifications_read(request, thread_id):
    try:
        thread = MessageThread.objects.get(
            Q(user1=request.user) | Q(user2=request.user),
            id=thread_id
        )
    except MessageThread.DoesNotExist:
        return JsonResponse({'error': 'Thread not found'}, status=404)

    # Mark notifications related to this thread as read
    Notification.objects.filter(user=request.user, thread=thread, is_read=False).update(is_read=True)

    # Return new unread count
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})