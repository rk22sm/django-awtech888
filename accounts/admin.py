from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile ,NotificationSettings ,Notification# Ensure both User and Profile are imported

# Register User model with custom admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'membership_plan', 'is_staff')
    list_filter = ('role', 'membership_plan', 'is_staff')

# Register Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'headline', 'location', 'created_at')
    list_filter = ('location', 'created_at')

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user'  # allows sorting by username
    get_username.short_description = 'Username'

@admin.register(NotificationSettings)
class NotificationAdmin(admin.ModelAdmin):
    list_display = "user", "email_notifications", "push_notifications"

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "actor", "verb", "is_read", "created_at")
    list_filter = ("is_read",)
