# # # # # import requests
# # # # # from datetime import datetime
# # # # # from django.conf import settings
# # # # # from rest_framework.views import APIView
# # # # # from rest_framework.response import Response
# # # # # from rest_framework import status
# # # # # from .models import Order
# # # # # from .serializers import OrderSerializer
# # # # #
# # # # # class OrderCreateAPI(APIView):
# # # # #     def get(self, request):
# # # # #         return Response({"message": "Send a POST request to create an order."})
# # # # #
# # # # #     def post(self, request):
# # # # #         serializer = OrderSerializer(data=request.data)
# # # # #         if serializer.is_valid():
# # # # #             order = serializer.save()
# # # # #
# # # # #             # Prepare ERP data
# # # # #             try:
# # # # #                 erp_data = {
# # # # #                     "doctype": "Sales Order",
# # # # #                     "customer": order.customer_name,
# # # # #                     "transaction_date": str(order.created_at.date()),  # auto-use created date
# # # # #                     "delivery_date": str(order.delivery_date),        # ✅ REQUIRED FIELD
# # # # #                     "items": [{
# # # # #                         "item_code": order.item,
# # # # #                         "qty": order.quantity
# # # # #                     }],
# # # # #                     "custom_order_type": order.order_type,
# # # # #                     "custom_vehicle_number": order.vehicle_number,
# # # # #                     "custom_warehouse": order.warehouse,
# # # # #                     "custom_delivery_address": order.delivery_address
# # # # #                 }
# # # # #
# # # # #                 headers = {
# # # # #                     "Authorization": f"token {settings.FRAPPE_API_KEY}:{settings.FRAPPE_SECRET_KEY}",
# # # # #                     "Content-Type": "application/json"
# # # # #                 }
# # # # #
# # # # #                 response = requests.post(
# # # # #                     f"{settings.FRAPPE_URL}/api/resource/Sales Order",
# # # # #                     json=erp_data,
# # # # #                     headers=headers,
# # # # #                     timeout=10
# # # # #                 )
# # # # #
# # # # #                 if response.status_code in [200, 201]:
# # # # #                     return Response({"message": "Order created and pushed to ERP"}, status=status.HTTP_201_CREATED)
# # # # #                 else:
# # # # #                     return Response({
# # # # #                         "message": "Order saved locally but ERP push failed",
# # # # #                         "status_code": response.status_code,
# # # # #                         "response": response.json()
# # # # #                     }, status=500)
# # # # #
# # # # #             except Exception as e:
# # # # #                 return Response({
# # # # #                     "message": "Order saved locally but failed to push to ERP",
# # # # #                     "error": str(e)
# # # # #                 }, status=500)
# # # # #
# # # # #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # # #
# # # # import requests
# # # # from datetime import datetime
# # # # from django.conf import settings
# # # # from django.http import JsonResponse
# # # # from rest_framework.views import APIView
# # # # from rest_framework.response import Response
# # # # from rest_framework import status
# # # # from .models import Order
# # # # from .serializers import OrderSerializer
# # # #
# # # #
# # # # # ✅ Root Health Check
# # # # def health_check(request):
# # # #     return JsonResponse({"status": "OK", "message": "ERP API is running."})
# # # #
# # # #
# # # # # ✅ Optional: Handle favicon.ico
# # # # def empty_favicon(request):
# # # #     return JsonResponse({}, status=204)
# # # #
# # # #
# # # # class OrderCreateAPI(APIView):
# # # #     def get(self, request):
# # # #         return Response({"message": "Send a POST request to create an order."})
# # # #
# # # #     def post(self, request):
# # # #         serializer = OrderSerializer(data=request.data)
# # # #         if serializer.is_valid():
# # # #             order = serializer.save()
# # # #
# # # #             try:
# # # #                 headers = {
# # # #                     "Authorization": f"token {settings.FRAPPE_API_KEY}:{settings.FRAPPE_SECRET_KEY}",
# # # #                     "Content-Type": "application/json"
# # # #                 }
# # # #
# # # #                 # ✅ Step 1: Create Sales Order
# # # #                 so_payload = {
# # # #                     "doctype": "Sales Order",
# # # #                     "customer": order.customer_name,
# # # #                     "transaction_date": str(order.created_at.date()),
# # # #                     "delivery_date": str(order.delivery_date),
# # # #                     "items": [{
# # # #                         "item_code": order.item,
# # # #                         "qty": order.quantity
# # # #                     }],
# # # #                     "custom_order_type": order.order_type,
# # # #                     "custom_vehicle_number": order.vehicle_number,
# # # #                     "custom_warehouse": order.warehouse,
# # # #                     "custom_delivery_address": order.delivery_address
# # # #                 }
# # # #
# # # #                 so_response = requests.post(
# # # #                     f"{settings.FRAPPE_URL}/api/resource/Sales Order",
# # # #                     json=so_payload,
# # # #                     headers=headers,
# # # #                     timeout=10
# # # #                 )
# # # #
# # # #                 if so_response.status_code not in [200, 201]:
# # # #                     return Response({
# # # #                         "message": "Order saved locally but ERP Sales Order push failed",
# # # #                         "response": so_response.json()
# # # #                     }, status=500)
# # # #
# # # #                 so_name = so_response.json()["data"]["name"]
# # # #
# # # #                 # ✅ Step 2: Create Sales Invoice
# # # #                 invoice_payload = {
# # # #                     "doctype": "Sales Invoice",
# # # #                     "customer": order.customer_name,
# # # #                     "items": [{
# # # #                         "item_code": order.item,
# # # #                         "qty": order.quantity,
# # # #                         "rate": 500  # Static for now; fetch from ERP if needed
# # # #                     }],
# # # #                     "due_date": str(order.delivery_date),
# # # #                     "set_posting_time": 1
# # # #                 }
# # # #
# # # #                 invoice_response = requests.post(
# # # #                     f"{settings.FRAPPE_URL}/api/resource/Sales Invoice",
# # # #                     json=invoice_payload,
# # # #                     headers=headers,
# # # #                     timeout=10
# # # #                 )
# # # #
# # # #                 if invoice_response.status_code not in [200, 201]:
# # # #                     return Response({
# # # #                         "message": "Sales Order created but Invoice failed",
# # # #                         "response": invoice_response.json()
# # # #                     }, status=500)
# # # #
# # # #                 invoice_name = invoice_response.json()["data"]["name"]
# # # #
# # # #                 # ✅ Step 3: Fetch Party Account
# # # #                 party_account_response = requests.get(
# # # #                     f"{settings.FRAPPE_URL}/api/method/erpnext.accounts.party.get_party_account",
# # # #                     headers=headers,
# # # #                     params={
# # # #                         "party_type": "Customer",
# # # #                         "party": order.customer_name,
# # # #                         "company": "Arun Indane Gas"  # 🔁 Replace with exact ERP companyss
# # # #                     },
# # # #                     timeout=10
# # # #                 )
# # # #
# # # #                 print("ERP Party Account Response:", party_account_response.json())
# # # #
# # # #                 if party_account_response.status_code != 200:
# # # #                     return Response({
# # # #                         "message": "Invoice created but failed to fetch Party Account",
# # # #                         "response": party_account_response.json()
# # # #                     }, status=500)
# # # #
# # # #                 party_account = party_account_response.json().get("message")
# # # #
# # # #                 if not party_account:
# # # #                     return Response({
# # # #                         "message": "Invoice created but no Party Account found for customer.",
# # # #                         "error": "Customer may not have a Receivable Account set in ERP.",
# # # #                         "erp_response": party_account_response.json()
# # # #                     }, status=500)
# # # #
# # # #                 print("✅ Resolved Party Account:", party_account)
# # # #
# # # #                 # ✅ Submit the Sales Invoice
# # # #                 submit_response = requests.post(
# # # #                     f"{settings.FRAPPE_URL}/api/method/frappe.client.submit",
# # # #                     headers=headers,
# # # #                     json={"doctype": "Sales Invoice", "name": invoice_name},
# # # #                     timeout=10
# # # #                 )
# # # #
# # # #                 if submit_response.status_code != 200:
# # # #                     return Response({
# # # #                         "message": "Invoice created but failed to submit",
# # # #                         "response": submit_response.json()
# # # #                     }, status=500)
# # # #
# # # #                 # ✅ Step 4: Create Payment Entry
# # # #                 payment_payload = {
# # # #                     "doctype": "Payment Entry",
# # # #                     "payment_type": "Receive",
# # # #                     "party_type": "Customer",
# # # #                     "party": order.customer_name,
# # # #                     "party_account": party_account,
# # # #                     "paid_amount": 500,
# # # #                     "received_amount": 500,
# # # #                     "mode_of_payment": "Cash",
# # # #                     "reference_no": f"AUTO-{invoice_name}",
# # # #                     "reference_date": str(datetime.today().date()),
# # # #                     "company": "Arun indane gas",  # 🔁 Match ERP company
# # # #                     "source_exchange_rate": 1.0,
# # # #                     "target_exchange_rate":1.0,
# # # #                     "references": [
# # # #                         {
# # # #                             "reference_doctype": "Sales Invoice",
# # # #                             "reference_name": invoice_name,
# # # #                             "allocated_amount": 500
# # # #                         }
# # # #                     ]
# # # #
# # # #                 }
# # # #
# # # #                 payment_response = requests.post(
# # # #                     f"{settings.FRAPPE_URL}/api/resource/Payment Entry",
# # # #                     json=payment_payload,
# # # #                     headers=headers,
# # # #                     timeout=10
# # # #                 )
# # # #
# # # #                 if payment_response.status_code not in [200, 201]:
# # # #                     return Response({
# # # #                         "message": "Invoice created but Payment failed",
# # # #                         "response": payment_response.json()
# # # #                     }, status=500)
# # # #
# # # #                 return Response({
# # # #                     "message": "Order, Invoice, and Payment successfully pushed to ERP",
# # # #                     "sales_order": so_name,
# # # #                     "invoice": invoice_name,
# # # #                     "payment_entry": payment_response.json()["data"]["name"]
# # # #                 }, status=201)
# # # #
# # # #             except Exception as e:
# # # #                 return Response({
# # # #                     "message": "Unexpected error during ERP sync",
# # # #                     "error": str(e)
# # # #                 }, status=500)
# # # #
# # # #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # # import requests
# # # from datetime import datetime
# # # from django.conf import settings
# # # from django.http import JsonResponse
# # # from rest_framework.views import APIView
# # # from rest_framework.response import Response
# # # from rest_framework import status
# # # from .models import Order
# # # from .serializers import OrderSerializer
# # #
# # #
# # # # ✅ Optional health check route
# # # def health_check(request):
# # #     return JsonResponse({"status": "OK", "message": "ERP API is running."})
# # #
# # #
# # # class OrderCreateAPI(APIView):
# # #     def get(self, request):
# # #         return Response({"message": "Send a POST request to create an order."})
# # #
# # #     def post(self, request):
# # #         serializer = OrderSerializer(data=request.data)
# # #         if serializer.is_valid():
# # #             order = serializer.save()
# # #
# # #             try:
# # #                 headers = {
# # #                     "Authorization": f"token {settings.FRAPPE_API_KEY}:{settings.FRAPPE_SECRET_KEY}",
# # #                     "Content-Type": "application/json"
# # #                 }
# # #
# # #                 # ✅ 1. Create Sales Order
# # #                 so_payload = {
# # #                     "doctype": "Sales Order",
# # #                     "customer": order.customer_name,
# # #                     "transaction_date": str(order.created_at.date()),
# # #                     "delivery_date": str(order.delivery_date),
# # #                     "items": [{
# # #                         "item_code": order.item,
# # #                         "qty": order.quantity
# # #                     }],
# # #                     "custom_order_type": order.order_type,
# # #                     "custom_vehicle_number": order.vehicle_number,
# # #                     "custom_warehouse": order.warehouse,
# # #                     "custom_delivery_address": order.delivery_address
# # #                 }
# # #
# # #                 so_response = requests.post(
# # #                     f"{settings.FRAPPE_URL}/api/resource/Sales Order",
# # #                     json=so_payload,
# # #                     headers=headers,
# # #                     timeout=10
# # #                 )
# # #
# # #                 if so_response.status_code not in [200, 201]:
# # #                     return Response({
# # #                         "message": "Order saved locally but ERP Sales Order push failed",
# # #                         "response": so_response.json()
# # #                     }, status=500)
# # #
# # #                 so_name = so_response.json()["data"]["name"]
# # #
# # #                 # ✅ 2. Create Sales Invoice
# # #                 invoice_payload = {
# # #                     "doctype": "Sales Invoice",
# # #                     "customer": order.customer_name,
# # #                     "items": [{
# # #                         "item_code": order.item,
# # #                         "qty": order.quantity,
# # #                         "rate": 500  # You can change this dynamically
# # #                     }],
# # #                     "due_date": str(order.delivery_date),
# # #                     "set_posting_time": 1
# # #                 }
# # #
# # #                 invoice_response = requests.post(
# # #                     f"{settings.FRAPPE_URL}/api/resource/Sales Invoice",
# # #                     json=invoice_payload,
# # #                     headers=headers,
# # #                     timeout=10
# # #                 )
# # #
# # #                 if invoice_response.status_code not in [200, 201]:
# # #                     return Response({
# # #                         "message": "Sales Order created but Invoice creation failed",
# # #                         "response": invoice_response.json()
# # #                     }, status=500)
# # #
# # #                 invoice_name = invoice_response.json()["data"]["name"]
# # #
# # #                 # ✅ 3. Submit Sales Invoice
# # #                 submit_response = requests.post(
# # #                     f"{settings.FRAPPE_URL}/api/resource/Sales Invoice/{invoice_name}?run_method=submit",
# # #                     headers=headers,
# # #                     timeout=10
# # #                 )
# # #
# # #                 if submit_response.status_code != 200:
# # #                     return Response({
# # #                         "message": "Invoice created but submission failed",
# # #                         "response": submit_response.json()
# # #                     }, status=500)
# # #
# # #                 # ✅ 4. Fetch Party Account
# # #                 party_account_response = requests.get(
# # #                     f"{settings.FRAPPE_URL}/api/method/erpnext.accounts.party.get_party_account",
# # #                     headers=headers,
# # #                     params={
# # #                         "party_type": "Customer",
# # #                         "party": order.customer_name,
# # #                         "company": "Arun Indane Gas"  # Change to your exact company name
# # #                     },
# # #                     timeout=10
# # #                 )
# # #
# # #                 if party_account_response.status_code != 200:
# # #                     return Response({
# # #                         "message": "Invoice submitted but failed to fetch Party Account",
# # #                         "response": party_account_response.json()
# # #                     }, status=500)
# # #
# # #                 party_account = party_account_response.json().get("message")
# # #
# # #                 if not party_account:
# # #                     return Response({
# # #                         "message": "Invoice submitted but no Party Account found for customer.",
# # #                         "error": "Customer may not have a Receivable Account set in ERP.",
# # #                         "erp_response": party_account_response.json()
# # #                     }, status=500)
# # #
# # #                 # ✅ 5. Create Payment Entry
# # #                 payment_payload = {
# # #                     "doctype": "Payment Entry",
# # #                     "payment_type": "Receive",
# # #                     "party_type": "Customer",
# # #                     "party": order.customer_name,
# # #                     "party_account": party_account,
# # #                     "paid_amount": 500,
# # #                     "received_amount": 500,
# # #                     "mode_of_payment": "Cash",
# # #                     "reference_no": f"AUTO-{invoice_name}",
# # #                     "reference_date": str(datetime.today().date()),
# # #                     "company": "Arun Indane Gas",  # Ensure this matches your ERP company
# # #                     "source_exchange_rate": 1.0,
# # #                     "target_exchange_rate": 1.0,
# # #                     "paid_to": "Cash - AIG",  # 🔁 Use your ERP’s actual cash/bank account
# # #                     "paid_to_account_currency": "INR",
# # #                     "references": [
# # #                         {
# # #                             "reference_doctype": "Sales Invoice",
# # #                             "reference_name": invoice_name,
# # #                             "allocated_amount": 500
# # #                         }
# # #                     ]
# # #                 }
# # #
# # #                 payment_response = requests.post(
# # #                     f"{settings.FRAPPE_URL}/api/resource/Payment Entry",
# # #                     json=payment_payload,
# # #                     headers=headers,
# # #                     timeout=10
# # #                 )
# # #
# # #                 if payment_response.status_code not in [200, 201]:
# # #                     return Response({
# # #                         "message": "Invoice submitted but Payment failed",
# # #                         "response": payment_response.json()
# # #                     }, status=500)
# # #
# # #                 return Response({
# # #                     "message": "Order, Invoice, and Payment successfully pushed to ERP",
# # #                     "sales_order": so_name,
# # #                     "invoice": invoice_name,
# # #                     "payment_entry": payment_response.json()["data"]["name"]
# # #                 }, status=201)
# # #
# # #             except Exception as e:
# # #                 return Response({
# # #                     "message": "Unexpected error during ERP sync",
# # #                     "error": str(e)
# # #                 }, status=500)
# # #
# # #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # import requests
# # from datetime import datetime
# # from django.conf import settings
# # from django.http import JsonResponse
# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from .models import Order
# # from .serializers import OrderSerializer
# #
# #
# # # Optional: Health check endpoint
# # def health_check(request):
# #     return JsonResponse({"status": "OK", "message": "ERP API is running."})
# #
# #
# # class OrderCreateAPI(APIView):
# #     def get(self, request):
# #         return Response({"message": "Send a POST request to create an order."})
# #
# #     def post(self, request):
# #         serializer = OrderSerializer(data=request.data)
# #         if serializer.is_valid():
# #             order = serializer.save()
# #
# #             try:
# #                 headers = {
# #                     "Authorization": f"token {settings.FRAPPE_API_KEY}:{settings.FRAPPE_SECRET_KEY}",
# #                     "Content-Type": "application/json"
# #                 }
# #
# #                 # 1. Create Sales Order
# #                 so_payload = {
# #                     "doctype": "Sales Order",
# #                     "customer": order.customer_name,
# #                     "transaction_date": str(order.created_at.date()),
# #                     "delivery_date": str(order.delivery_date),
# #                     "items": [{
# #                         "item_code": order.item,
# #                         "qty": order.quantity
# #                     }],
# #                     "custom_order_type": order.order_type,
# #                     "custom_vehicle_number": order.vehicle_number,
# #                     "custom_warehouse": order.warehouse,
# #                     "custom_delivery_address": order.delivery_address
# #                 }
# #
# #                 so_response = requests.post(
# #                     f"{settings.FRAPPE_URL}/api/resource/Sales Order",
# #                     json=so_payload,
# #                     headers=headers,
# #                     timeout=10
# #                 )
# #
# #                 if so_response.status_code not in [200, 201]:
# #                     return Response({
# #                         "message": "Order saved locally but ERP Sales Order push failed",
# #                         "response": so_response.json()
# #                     }, status=500)
# #
# #                 so_name = so_response.json()["data"]["name"]
# #
# #                 # 2. Create Sales Invoice
# #                 invoice_payload = {
# #                     "doctype": "Sales Invoice",
# #                     "customer": order.customer_name,
# #                     "items": [{
# #                         "item_code": order.item,
# #                         "qty": order.quantity
# #                     }],
# #                     "due_date": str(order.delivery_date),
# #                     "set_posting_time": 1
# #                 }
# #
# #                 invoice_response = requests.post(
# #                     f"{settings.FRAPPE_URL}/api/resource/Sales Invoice",
# #                     json=invoice_payload,
# #                     headers=headers,
# #                     timeout=10
# #                 )
# #
# #                 if invoice_response.status_code not in [200, 201]:
# #                     return Response({
# #                         "message": "Sales Order created but Invoice creation failed",
# #                         "response": invoice_response.json()
# #                     }, status=500)
# #
# #                 invoice_data = invoice_response.json()["data"]
# #                 invoice_name = invoice_data["name"]
# #                 invoice_total = invoice_data.get("grand_total", 0)
# #
# #                 # 3. Submit the Invoice
# #                 submit_response = requests.post(
# #                     f"{settings.FRAPPE_URL}/api/resource/Sales Invoice/{invoice_name}?run_method=submit",
# #                     headers=headers,
# #                     timeout=10
# #                 )
# #
# #                 if submit_response.status_code != 200:
# #                     return Response({
# #                         "message": "Invoice created but submission failed",
# #                         "response": submit_response.json()
# #                     }, status=500)
# #
# #                 # 4. Fetch Party Account
# #                 party_account_response = requests.get(
# #                     f"{settings.FRAPPE_URL}/api/method/erpnext.accounts.party.get_party_account",
# #                     headers=headers,
# #                     params={
# #                         "party_type": "Customer",
# #                         "party": order.customer_name,
# #                         "company": "Arun Indane Gas"  # Replace with your ERP company name
# #                     },
# #                     timeout=10
# #                 )
# #
# #                 if party_account_response.status_code != 200:
# #                     return Response({
# #                         "message": "Invoice submitted but failed to fetch Party Account",
# #                         "response": party_account_response.json()
# #                     }, status=500)
# #
# #                 party_account = party_account_response.json().get("message")
# #                 if not party_account:
# #                     return Response({
# #                         "message": "Invoice submitted but no Party Account found for customer.",
# #                         "error": "Customer may not have a Receivable Account set in ERP.",
# #                         "erp_response": party_account_response.json()
# #                     }, status=500)
# #
# #                 # 5. Create Payment Entry (use grand_total dynamically)
# #                 payment_payload = {
# #                     "doctype": "Payment Entry",
# #                     "payment_type": "Receive",
# #                     "party_type": "Customer",
# #                     "party": order.customer_name,
# #                     "party_account": party_account,
# #                     "paid_amount": invoice_total,
# #                     "received_amount": invoice_total,
# #                     "mode_of_payment": "Cash",
# #                     "reference_no": f"AUTO-{invoice_name}",
# #                     "reference_date": str(datetime.today().date()),
# #                     "company": "Arun Indane Gas",  # Must match your ERP company
# #                     "source_exchange_rate": 1.0,
# #                     "target_exchange_rate": 1.0,
# #                     "paid_to": "Cash - AIG",  # Replace with valid ERP account
# #                     "paid_to_account_currency": "INR",
# #                     "references": [
# #                         {
# #                             "reference_doctype": "Sales Invoice",
# #                             "reference_name": invoice_name,
# #                             "allocated_amount": invoice_total
# #                         }
# #                     ]
# #                 }
# #
# #                 payment_response = requests.post(
# #                     f"{settings.FRAPPE_URL}/api/resource/Payment Entry",
# #                     json=payment_payload,
# #                     headers=headers,
# #                     timeout=10
# #                 )
# #
# #                 if payment_response.status_code not in [200, 201]:
# #                     return Response({
# #                         "message": "Invoice submitted but Payment failed",
# #                         "response": payment_response.json()
# #                     }, status=500)
# #
# #                 return Response({
# #                     "message": "Order, Invoice, and Payment successfully pushed to ERP",
# #                     "sales_order": so_name,
# #                     "invoice": invoice_name,
# #                     "payment_entry": payment_response.json()["data"]["name"]
# #                 }, status=201)
# #
# #             except Exception as e:
# #                 return Response({
# #                     "message": "Unexpected error during ERP sync",
# #                     "error": str(e)
# #                 }, status=500)
# #
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
# # Optional: Health check endpoint
# def health_check(request):
#     return JsonResponse({"status": "OK", "message": "ERP API is running."})
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
#                 # 1. Create Sales Order
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
#                 # Submit Sales Order
#                 submit_so_response = requests.post(
#                     f"{settings.FRAPPE_URL}/api/resource/Sales Order/{so_name}?run_method=submit",
#                     headers=headers,
#                     timeout=10
#                 )
#
#                 if submit_so_response.status_code != 200:
#                     return Response({
#                         "message": "Sales Order created but submission failed",
#                         "response": submit_so_response.json()
#                     }, status=500)
#
#                 # 2. Create Sales Invoice with Payment Terms Template
#                 invoice_payload = {
#                     "doctype": "Sales Invoice",
#                     "customer": order.customer_name,
#                     "items": [{
#                         "item_code": order.item,
#                         "qty": order.quantity
#                     }],
#                     "due_date": str(order.delivery_date),
#                     "set_posting_time": 1,
#                     "payment_terms_template": "CWO"
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
#                         "message": "Sales Order submitted but Invoice creation failed",
#                         "response": invoice_response.json()
#                     }, status=500)
#
#                 invoice_data = invoice_response.json()["data"]
#                 invoice_name = invoice_data["name"]
#                 invoice_total = invoice_data.get("grand_total", 0)
#
#                 # 3. Submit Sales Invoice
#                 submit_invoice_response = requests.post(
#                     f"{settings.FRAPPE_URL}/api/resource/Sales Invoice/{invoice_name}?run_method=submit",
#                     headers=headers,
#                     timeout=10
#                 )
#
#                 if submit_invoice_response.status_code != 200:
#                     return Response({
#                         "message": "Invoice created but submission failed",
#                         "response": submit_invoice_response.json()
#                     }, status=500)
#
#                 # 4. Fetch Party Account
#                 party_account_response = requests.get(
#                     f"{settings.FRAPPE_URL}/api/method/erpnext.accounts.party.get_party_account",
#                     headers=headers,
#                     params={
#                         "party_type": "Customer",
#                         "party": order.customer_name,
#                         "company": "Arun Indane Gas"
#                     },
#                     timeout=10
#                 )
#
#                 if party_account_response.status_code != 200:
#                     return Response({
#                         "message": "Invoice submitted but failed to fetch Party Account",
#                         "response": party_account_response.json()
#                     }, status=500)
#
#                 party_account = party_account_response.json().get("message")
#
#                 if not party_account:
#                     return Response({
#                         "message": "Invoice submitted but no Party Account found for customer.",
#                         "error": "Customer may not have a Receivable Account set in ERP.",
#                         "erp_response": party_account_response.json()
#                     }, status=500)
#
#                 # 5. Create Payment Entry with dynamic grand_total
#                 payment_payload = {
#                     "doctype": "Payment Entry",
#                     "payment_type": "Receive",
#                     "party_type": "Customer",
#                     "party": order.customer_name,
#                     "party_account": party_account,
#                     "paid_amount": invoice_total,
#                     "received_amount": invoice_total,
#                     "mode_of_payment": "Cash",
#                     "reference_no": f"AUTO-{invoice_name}",
#                     "reference_date": str(datetime.today().date()),
#                     "company": "Arun Indane Gas",
#                     "source_exchange_rate": 1.0,
#                     "target_exchange_rate": 1.0,
#                     "paid_to": "Cash - AIG",
#                     "paid_to_account_currency": "INR",
#                     "references": [
#                         {
#                             "reference_doctype": "Sales Invoice",
#                             "reference_name": invoice_name,
#                             "allocated_amount": invoice_total
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
#                         "message": "Invoice submitted but Payment failed",
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
import requests
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer


def health_check(request):
    return JsonResponse({"status": "OK", "message": "ERP API is running."})


class OrderCreateAPI(APIView):
    def get(self, request):
        return Response({"message": "Send a POST request to create an order."})

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            try:
                headers = {
                    "Authorization": f"token {settings.FRAPPE_API_KEY}:{settings.FRAPPE_SECRET_KEY}",
                    "Content-Type": "application/json"
                }

                # 1. Create Sales Order
                so_payload = {
                    "doctype": "Sales Order",
                    "customer": order.customer_name,
                    "transaction_date": str(order.created_at.date()),
                    "delivery_date": str(order.delivery_date),
                    "items": [{
                        "item_code": order.item,
                        "qty": order.quantity
                    }],
                    "custom_order_type": order.order_type,
                    "custom_vehicle_number": order.vehicle_number,
                    "custom_warehouse": order.warehouse,
                    "custom_delivery_address": order.delivery_address
                }

                so_response = requests.post(
                    f"{settings.FRAPPE_URL}/api/resource/Sales Order",
                    json=so_payload,
                    headers=headers,
                    timeout=10
                )

                if so_response.status_code not in [200, 201]:
                    return Response({
                        "message": "ERP Sales Order creation failed",
                        "response": so_response.json()
                    }, status=500)

                so_data = so_response.json()["data"]
                so_name = so_data["name"]
                so_grand_total = so_data.get("grand_total", 0)

                # Submit Sales Order
                submit_so_response = requests.post(
                    f"{settings.FRAPPE_URL}/api/resource/Sales Order/{so_name}?run_method=submit",
                    headers=headers,
                    timeout=10
                )

                if submit_so_response.status_code != 200:
                    return Response({
                        "message": "Sales Order created but submission failed",
                        "response": submit_so_response.json()
                    }, status=500)

                # 2. Fetch Party Account
                party_account_response = requests.get(
                    f"{settings.FRAPPE_URL}/api/method/erpnext.accounts.party.get_party_account",
                    headers=headers,
                    params={
                        "party_type": "Customer",
                        "party": order.customer_name,
                        "company": "Arun Indane Gas"
                    },
                    timeout=10
                )

                if party_account_response.status_code != 200:
                    return Response({
                        "message": "Failed to fetch Party Account",
                        "response": party_account_response.json()
                    }, status=500)

                party_account = party_account_response.json().get("message")
                if not party_account:
                    return Response({
                        "message": "No Party Account found for customer.",
                        "error": "Customer may not have a Receivable Account set in ERP.",
                        "erp_response": party_account_response.json()
                    }, status=500)

                # 3. Create Payment Entry linked to Sales Order
                payment_payload = {
                    "doctype": "Payment Entry",
                    "payment_type": "Receive",
                    "party_type": "Customer",
                    "party": order.customer_name,
                    "party_account": party_account,
                    "paid_amount": so_grand_total,
                    "received_amount": so_grand_total,
                    "mode_of_payment": "Cash",
                    "reference_no": f"AUTO-{so_name}",
                    "reference_date": str(datetime.today().date()),
                    "company": "Arun Indane Gas",
                    "source_exchange_rate": 1.0,
                    "target_exchange_rate": 1.0,
                    "paid_to": "Cash - AIG",
                    "paid_to_account_currency": "INR",
                    "references": [
                        {
                            "reference_doctype": "Sales Order",
                            "reference_name": so_name,
                            "allocated_amount": so_grand_total
                        }
                    ]
                }

                payment_response = requests.post(
                    f"{settings.FRAPPE_URL}/api/resource/Payment Entry",
                    json=payment_payload,
                    headers=headers,
                    timeout=10
                )

                if payment_response.status_code not in [200, 201]:
                    return Response({
                        "message": "Payment Entry creation failed",
                        "response": payment_response.json()
                    }, status=500)

                payment_name = payment_response.json()["data"]["name"]

                # 4. Create and Submit Sales Invoice linked to Sales Order
                invoice_payload = {
                    "doctype": "Sales Invoice",
                    "customer": order.customer_name,
                    "sales_order": so_name,
                    "items": [{
                        "item_code": order.item,
                        "qty": order.quantity
                    }],
                    "due_date": str(order.delivery_date),
                    "set_posting_time": 1
                }

                invoice_response = requests.post(
                    f"{settings.FRAPPE_URL}/api/resource/Sales Invoice",
                    json=invoice_payload,
                    headers=headers,
                    timeout=10
                )

                if invoice_response.status_code not in [200, 201]:
                    return Response({
                        "message": "Sales Invoice creation failed",
                        "response": invoice_response.json()
                    }, status=500)

                invoice_name = invoice_response.json()["data"]["name"]

                submit_response = requests.post(
                    f"{settings.FRAPPE_URL}/api/resource/Sales Invoice/{invoice_name}?run_method=submit",
                    headers=headers,
                    timeout=10
                )

                if submit_response.status_code != 200:
                    return Response({
                        "message": "Invoice submission failed",
                        "response": submit_response.json()
                    }, status=500)

                return Response({
                    "message": "Order, Payment, and Invoice successfully processed in ERP",
                    "sales_order": so_name,
                    "payment_entry": payment_name,
                    "invoice": invoice_name
                }, status=201)

            except Exception as e:
                return Response({
                    "message": "Unexpected error during ERP sync",
                    "error": str(e)
                }, status=500)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
