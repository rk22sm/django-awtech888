from django.urls import path
from . import views



app_name = 'connectpro'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('discover/', views.discover, name="discover"),
    path('edit_profile/', views.edit_profile, name="edit_profile")
    
]
