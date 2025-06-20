import requests
import json

# ✅ Wrap all these in strings
FRAPPE_URL = "https://ops.arungas.com"
FRAPPE_API_KEY = "134c3b1ba9df180"
FRAPPE_API_SECRET = "9fafb36f60f9f2e"

def push_order_to_erp(order):
    """Push approved order to ERP system"""
    if order.status != "approved":
        return False  # Only approved orders are pushed

    headers = {
        "Authorization": f"token {FRAPPE_API_KEY}:{FRAPPE_API_SECRET}",
        "Content-Type": "application/json"
    }

    payload = {
        "doctype": "Sales Order",
        "customer": order.customer_name,
        "items": [
            {
                "item_name": order.item,
                "qty": order.quantity,
            }
        ],
        "delivery_address": order.delivery_address,
        "warehouse": order.warehouse,
        "vehicle_number": order.vehicle_number,
    }

    try:
        response = requests.post(
            f"{FRAPPE_URL}/api/resource/Sales Order",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print("Failed to push order to ERP:", e)
        return False
