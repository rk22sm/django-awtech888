from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
# payments/views.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import os
User = get_user_model()

@csrf_exempt
def revenuecat_webhook(request):
    payload = json.loads(request.body)

    # Event example: "INITIAL_PURCHASE", "PRODUCT_PURCHASED", "CANCELLATION"
    event_type = payload.get("event")
    subscriber = payload.get("subscriber")
    user_id = subscriber.get("original_app_user_id")
    entitlements = subscriber.get("entitlements", {})

    try:
        user = User.objects.get(username=user_id)  # or another unique ID
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    # Example: update membership plan based on RevenueCat entitlement
    if "pro_entitlement" in entitlements:
        user.membership_plan = User.Membership.PRO
    elif "plus_entitlement" in entitlements:
        user.membership_plan = User.Membership.PLUS
    else:
        user.membership_plan = User.Membership.FREE

    user.save()

    return JsonResponse({"status": "success"})


User = get_user_model()
REVENUECAT_API_KEY = os.getenv("REVENUECAT_API_KEY")
BASE_URL = "https://api.revenuecat.com/v1"

HEADERS = {
    "Authorization": f"Bearer {REVENUECAT_API_KEY}",
    "Content-Type": "application/json",
}

@csrf_exempt
@login_required
def subscribe(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)
    plan = data.get("plan")
    user = request.user

    # Map frontend plan to RevenueCat product_id
    product_ids = {
        "free": "free_plan",
        "plus": "plus_plan",
        "pro": "pro_plan"
    }

    product_id = product_ids.get(plan)
    if not product_id:
        return JsonResponse({"error": "Invalid plan"}, status=400)

    # Here you could create a RevenueCat subscriber if not exists
    # or just trust the webhook for real purchase confirmation

    # For demo, we'll just update user's membership_plan
    user.membership_plan = plan
    user.save()

    return JsonResponse({"success": True})
