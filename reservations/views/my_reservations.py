from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation
import jdatetime


def jalali(date_value):
    if not date_value:
        return '-'
    if hasattr(date_value, 'date'):
        date_value = date_value.date()
    return jdatetime.date.fromgregorian(date=date_value).strftime('%Y/%m/%d')


@login_required
def my_reservations_view(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    for r in reservations:
        r.jalali_check_in = jalali(r.check_in)
        r.jalali_check_out = jalali(r.check_out)

    return render(request, 'reservations/my_reservations.html', {
        'reservations': reservations,
        'active_tab': 'reservations',
    })