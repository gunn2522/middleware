from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'approved'
        order.approved_by = request.user
        order.save()
        # TODO: Send notification
        return Response({'message': 'Order approved successfully'})
    except ObjectDoesNotExist:
        return Response({'error': 'Order not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'rejected'
        order.approved_by = request.user
        order.justification = request.data.get('justification', '')
        order.save()
        # TODO: Send notification
        return Response({'message': 'Order rejected successfully'})
    except ObjectDoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    from django.core.mail import send_mail

    send_mail(
        subject='Order Update',
        message=f'Your order #{order.id} has been {order.status}.',
        from_email='noreply@company.com',
        recipient_list=[order.user.email],
        fail_silently=True
    )


from django.shortcuts import render
from orders.models import Order

def manager_dashboard(request):
    pending_orders = Order.objects.filter(status='pending')
    return render(request, 'approvals/dashboard.html', {'orders': pending_orders})

