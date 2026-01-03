# payments/urls.py
from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("revenuecat-webhook/", views.revenuecat_webhook, name="revenuecat_webhook"),
     path("subscribe/", views.subscribe, name="subscribe"),
]
