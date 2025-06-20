import requests
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer

class OrderCreateAPI(APIView):
    def get(self, request):
        return Response({"message": "Send a POST request to create an order."})

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Prepare ERP data
            try:
                erp_data = {
                    "doctype": "Sales Order",
                    "customer": order.customer_name,
                    "transaction_date": str(order.created_at.date()),  # auto-use created date
                    "delivery_date": str(order.delivery_date),        # ✅ REQUIRED FIELD
                    "items": [{
                        "item_code": order.item,
                        "qty": order.quantity
                    }],
                    "custom_order_type": order.order_type,
                    "custom_vehicle_number": order.vehicle_number,
                    "custom_warehouse": order.warehouse,
                    "custom_delivery_address": order.delivery_address
                }

                headers = {
                    "Authorization": f"token {settings.FRAPPE_API_KEY}:{settings.FRAPPE_SECRET_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post(
                    f"{settings.FRAPPE_URL}/api/resource/Sales Order",
                    json=erp_data,
                    headers=headers,
                    timeout=10
                )

                if response.status_code in [200, 201]:
                    return Response({"message": "Order created and pushed to ERP"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        "message": "Order saved locally but ERP push failed",
                        "status_code": response.status_code,
                        "response": response.json()
                    }, status=500)

            except Exception as e:
                return Response({
                    "message": "Order saved locally but failed to push to ERP",
                    "error": str(e)
                }, status=500)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# import requests
# from datetime import datetime
# from django.conf import settings
# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Order
# from .serializers import OrderSerializer
#
#
# # ✅ Root Health Check
# def health_check(request):
#     return JsonResponse({"status": "OK", "message": "ERP API is running."})
#
#
# # ✅ Optional: Handle favicon.ico
# def empty_favicon(request):
#     return JsonResponse({}, status=204)
#
#
# class OrderCreateAPI(APIView):
#     def get(self, request):
#         return Response({"message": "Send a POST request to create an order."})
#
#     def post(self, request):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             order = serializer.save()
#
#             try:
#                 headers = {
#                     "Authorization": f"token {settings.FRAPPE_API_KEY}:{settings.FRAPPE_SECRET_KEY}",
#                     "Content-Type": "application/json"
#                 }
#
#                 # ✅ Step 1: Create Sales Order
#                 so_payload = {
#                     "doctype": "Sales Order",
#                     "customer": order.customer_name,
#                     "transaction_date": str(order.created_at.date()),
#                     "delivery_date": str(order.delivery_date),
#                     "items": [{
#                         "item_code": order.item,
#                         "qty": order.quantity
#                     }],
#                     "custom_order_type": order.order_type,
#                     "custom_vehicle_number": order.vehicle_number,
#                     "custom_warehouse": order.warehouse,
#                     "custom_delivery_address": order.delivery_address
#                 }
#
#                 so_response = requests.post(
#                     f"{settings.FRAPPE_URL}/api/resource/Sales Order",
#                     json=so_payload,
#                     headers=headers,
#                     timeout=10
#                 )
#
#                 if so_response.status_code not in [200, 201]:
#                     return Response({
#                         "message": "Order saved locally but ERP Sales Order push failed",
#                         "response": so_response.json()
#                     }, status=500)
#
#                 so_name = so_response.json()["data"]["name"]
#
#                 # ✅ Step 2: Create Sales Invoice
#                 invoice_payload = {
#                     "doctype": "Sales Invoice",
#                     "customer": order.customer_name,
#                     "items": [{
#                         "item_code": order.item,
#                         "qty": order.quantity,
#                         "rate": 500  # Static for now; fetch from ERP if needed
#                     }],
#                     "due_date": str(order.delivery_date),
#                     "set_posting_time": 1
#                 }
#
#                 invoice_response = requests.post(
#                     f"{settings.FRAPPE_URL}/api/resource/Sales Invoice",
#                     json=invoice_payload,
#                     headers=headers,
#                     timeout=10
#                 )
#
#                 if invoice_response.status_code not in [200, 201]:
#                     return Response({
#                         "message": "Sales Order created but Invoice failed",
#                         "response": invoice_response.json()
#                     }, status=500)
#
#                 invoice_name = invoice_response.json()["data"]["name"]
#
#                 # ✅ Step 3: Fetch Party Account
#                 party_account_response = requests.get(
#                     f"{settings.FRAPPE_URL}/api/method/erpnext.accounts.party.get_party_account",
#                     headers=headers,
#                     params={
#                         "party_type": "Customer",
#                         "party": order.customer_name,
#                         "company": "Your Company Name"  # 🔁 Replace with exact ERP company
#                     },
#                     timeout=10
#                 )
#
#                 print("ERP Party Account Response:", party_account_response.json())
#
#                 if party_account_response.status_code != 200:
#                     return Response({
#                         "message": "Invoice created but failed to fetch Party Account",
#                         "response": party_account_response.json()
#                     }, status=500)
#
#                 party_account = party_account_response.json().get("message")
#
#                 if not party_account:
#                     return Response({
#                         "message": "Invoice created but no Party Account found for customer.",
#                         "error": "Customer may not have a Receivable Account set in ERP.",
#                         "erp_response": party_account_response.json()
#                     }, status=500)
#
#                 print("✅ Resolved Party Account:", party_account)
#
#                 # ✅ Step 4: Create Payment Entry
#                 payment_payload = {
#                     "doctype": "Payment Entry",
#                     "payment_type": "Receive",
#                     "party_type": "Customer",
#                     "party": order.customer_name,
#                     "party_account": party_account,
#                     "paid_amount": 500,
#                     "received_amount": 500,
#                     "mode_of_payment": "Cash",
#                     "reference_no": f"AUTO-{invoice_name}",
#                     "reference_date": str(datetime.today().date()),
#                     "company": "Arun indane gas",  # 🔁 Match ERP company
#                     "source_exchange_rate": 1.0,
#                     "references": [
#                         {
#                             "reference_doctype": "Sales Invoice",
#                             "reference_name": invoice_name,
#                             "allocated_amount": 500
#                         }
#                     ]
#                 }
#
#                 payment_response = requests.post(
#                     f"{settings.FRAPPE_URL}/api/resource/Payment Entry",
#                     json=payment_payload,
#                     headers=headers,
#                     timeout=10
#                 )
#
#                 if payment_response.status_code not in [200, 201]:
#                     return Response({
#                         "message": "Invoice created but Payment failed",
#                         "response": payment_response.json()
#                     }, status=500)
#
#                 return Response({
#                     "message": "Order, Invoice, and Payment successfully pushed to ERP",
#                     "sales_order": so_name,
#                     "invoice": invoice_name,
#                     "payment_entry": payment_response.json()["data"]["name"]
#                 }, status=201)
#
#             except Exception as e:
#                 return Response({
#                     "message": "Unexpected error during ERP sync",
#                     "error": str(e)
#                 }, status=500)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
