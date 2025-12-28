from django.urls import path
from . import views



app_name = 'connectpro'

urlpatterns = [
    path('', views.profile, name='profile'),
    
]
