from django.utils import timezone
from .models import Connection

def get_daily_connection_stats(user):
    """Return (limit, remaining) for today based on membership."""
    limit = user.daily_connection_limit()  # returns None for Pro (unlimited)

    if limit is None:
        return None, None

    today = timezone.now().date()
    used = Connection.objects.filter(
        from_user=user,
        created_at__date=today
    ).count()

    remaining = max(limit - used, 0)
    return limit, remaining
