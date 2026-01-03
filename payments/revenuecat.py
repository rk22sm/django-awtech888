# payments/revenuecat.py
import os
import requests

REVENUECAT_API_KEY = os.getenv("REVENUECAT_API_KEY")
BASE_URL = "https://api.revenuecat.com/v1"

HEADERS = {
    "Authorization": f"Bearer {REVENUECAT_API_KEY}",
    "Content-Type": "application/json",
}

def get_customer(user_id):
    """Fetch user data from RevenueCat."""
    url = f"{BASE_URL}/subscribers/{user_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def grant_entitlement(user_id, entitlement_id):
    """Optional: manually grant entitlement if needed."""
    url = f"{BASE_URL}/subscribers/{user_id}/entitlements/{entitlement_id}"
    response = requests.post(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()
