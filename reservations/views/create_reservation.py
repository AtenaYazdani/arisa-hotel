import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rooms.models import RoomType
from reservations.forms.reservation_form import ReservationForm
from reservations.models import Reservation, ReservationGuest
from reservations.services.availability_service import is_room_available
from core.services.email_service import send_reservation_confirmation_email
import jdatetime
logger = logging.getLogger('reservations')


def to_jalali_str(date_value):
    return jdatetime.date.fromgregorian(date=date_value).strftime('%Y/%m/%d')

@login_required
def create_reservation_view(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id, is_active=True)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            if not is_room_available(room_type, check_in, check_out):
                messages.error(request, 'این اتاق برای بازه‌ی انتخابی شما تکمیل ظرفیت است.')
                logger.info(f'رزرو ناموفق (ظرفیت تکمیل) - اتاق {room_type.code} توسط {request.user.phone}')
                return redirect('rooms:detail', room_type.id)

            reservation = Reservation.objects.create(
                user=request.user,
                room_type=room_type,
                check_in=check_in,
                check_out=check_out,
                note=form.cleaned_data.get('note', ''),
            )

            guest_names_raw = form.cleaned_data.get('guest_names', '')
            for name in guest_names_raw.splitlines():
                name = name.strip()
                if name:
                    ReservationGuest.objects.create(reservation=reservation, full_name=name)

            nights_count = (check_out - check_in).days
            send_reservation_confirmation_email(
                to_email=request.user.email,
                room_name=room_type.name,
                check_in=to_jalali_str(check_in),
                check_out=to_jalali_str(check_out),
                nights_count=nights_count,
                confirmation_code=reservation.confirmation_code,
            )

            logger.info(f'رزرو موفق - اتاق {room_type.code} توسط {request.user.phone} (کد: {reservation.confirmation_code})')
            messages.success(request, f'رزرو شما با موفقیت ثبت شد. کد تأیید: {reservation.confirmation_code}')
            return redirect('reservations:my_reservations')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('rooms:detail', room_type.id)

    return redirect('rooms:detail', room_type.id)