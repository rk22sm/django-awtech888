from django.urls import path
from . import views

app_name = "messages"

urlpatterns = [
    path("", views.inbox, name="inbox"),  # Shows inbox + active thread
    path("start/<int:user_id>/", views.start_chat, name="start_chat"),  # Starts new thread
    path("send/<int:thread_id>/", views.send_message, name="send_message"),  # NEW
    path('api/mark_thread_read/<int:thread_id>/', views.mark_thread_notifications_read, name='mark_thread_read'),
]



#https://www.oodlestechnologies.com/dev-blog/how-to-make-chat-application-in-django./ 2025-12-30 
