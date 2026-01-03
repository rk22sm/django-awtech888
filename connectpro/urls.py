from django.urls import path
from . import views



app_name = 'connectpro'

urlpatterns = [
    path('', views.profile, name='profile'),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path('discover/', views.discover, name="discover"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path("connect/<str:username>/", views.connect, name="connect"),
    path("respond_connection/<int:connection_id>/", views.respond_connection, name="respond_connection"),
    path("profile/<int:user_id>/", views.profile_detail, name="profile_detail"),
    path("connections/json/", views.connections_json, name="connections_json"),

]
