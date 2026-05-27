from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from apps.orders.models import Order, OrderItem
from apps.boxes.models import Box
from .models import Booking, SupportRequest

@login_required
def book_box(request, box_id):
    box = get_object_or_404(Box, id=box_id)

    if request.method == 'POST':
        start = request.POST.get('start_time')
        duration = int(request.POST.get('duration') or 1)
        start_dt = parse_datetime(start)

        if timezone.is_naive(start_dt):
            start_dt = timezone.make_aware(start_dt)

        if start_dt < timezone.now():
            messages.error(request, "Không thể đặt lịch trong quá khứ!")
            return redirect('home')

        end_dt = start_dt + timedelta(hours=duration)
        overlapping = Booking.objects.filter(
            box=box,
            status__in=['pending', 'confirmed', 'active', 'cancellation_pending']
        ).filter(Q(start_time__lt=end_dt) & Q(end_time__gt=start_dt))

        if overlapping.exists():
            messages.error(request, "Box đã bị đặt trong khung giờ này!")
        else:
            Booking.objects.create(
                customer=request.user,
                box=box,
                start_time=start_dt,
                end_time=end_dt,
                status='pending',
            )
            box.status = 'pending'
            box.save(update_fields=['status'])
            messages.success(request, "Yêu cầu đặt box đã được gửi, vui lòng chờ admin/staff phê duyệt.")

        return redirect('home')

    return render(request, 'bookings/book.html', {'box': box})


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    orders = Order.objects.filter(booking=booking).prefetch_related('items').order_by('-created_at')
    items = OrderItem.objects.filter(order__in=orders)

    booking_fee = booking.total_price
    order_total = sum(order.total_price for order in orders)
    grand_total = booking_fee + order_total

    for item in items:
        item.total_item_price = item.price * item.quantity

    return render(request, 'bookings/booking_detail.html', {
        'booking': booking,
        'orders': orders,
        'items': items,
        'order_total': order_total,
        'booking_fee': booking_fee,
        'grand_total': grand_total,
    })


def send_support_request(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        message = request.POST.get('message')

        if message:
            SupportRequest.objects.create(booking=booking, message=message)
            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Vui lòng nhập nội dung'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Phương thức không hợp lệ'}, status=400)


@login_required
def request_booking_cancellation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method != 'POST':
        return redirect('home')

    if booking.status not in {'pending', 'confirmed'}:
        messages.error(request, "Chỉ có thể yêu cầu hủy đơn đang chờ phê duyệt hoặc chờ check-in.")
        return redirect('home')

    reason = request.POST.get('reason', '').strip()
    if not reason:
        messages.error(request, "Vui lòng chọn lý do hủy đơn.")
        return redirect('home')

    booking.cancellation_previous_status = booking.status
    booking.status = 'cancellation_pending'
    booking.cancellation_reason = reason
    booking.cancellation_requested_at = timezone.now()
    booking.cancellation_response_message = ''
    booking.save(update_fields=[
        'status',
        'cancellation_reason',
        'cancellation_requested_at',
        'cancellation_previous_status',
        'cancellation_response_message',
    ])
    booking.box.status = 'pending'
    booking.box.save(update_fields=['status'])
    messages.success(request, "Yêu cầu hủy của bạn đã được nhận, chúng tôi sẽ xử lý trong 15 phút.")
    return redirect('home')
def send_support_request(request, booking_id):
    if request.method == 'POST':
        # Dùng get_object_or_404 để tránh lỗi nếu ID không tồn tại
        booking = get_object_or_404(Booking, id=booking_id)
        message = request.POST.get('message')
        
        if message:
            SupportRequest.objects.create(booking=booking, message=message)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Vui lòng nhập nội dung'}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Phương thức không hợp lệ'}, status=400)


@login_required
def request_booking_cancellation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method != 'POST':
        return redirect('home')

    if booking.status not in {'pending', 'confirmed'}:
        messages.error(request, "Chỉ có thể yêu cầu hủy đơn đang chờ phê duyệt hoặc chờ check-in.")
        return redirect('home')

    reason = request.POST.get('reason', '').strip()
    if not reason:
        messages.error(request, "Vui lòng chọn lý do hủy đơn.")
        return redirect('home')

    booking.cancellation_previous_status = booking.status
    booking.status = 'cancellation_pending'
    booking.cancellation_reason = reason
    booking.cancellation_requested_at = timezone.now()
    booking.cancellation_response_message = ''
    booking.save(update_fields=[
        'status',
        'cancellation_reason',
        'cancellation_requested_at',
        'cancellation_previous_status',
        'cancellation_response_message',
    ])
    booking.box.status = 'pending'
    booking.box.save(update_fields=['status'])
    messages.success(request, "Yêu cầu hủy của bạn đã được nhận, chúng tôi sẽ xử lý trong 15 phút.")
    return redirect('home')



    
