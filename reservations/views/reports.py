import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from reservations.forms.report_form import ReservationReportForm, FinancialReportForm
from reservations.models import Reservation
from reservations.services.pdf_service import build_pdf_table

logger = logging.getLogger('reservations')


def is_admin(user):
    return user.is_authenticated and user.role in ('admin_main', 'admin_reservation')


@login_required
@user_passes_test(is_admin)
def reservation_report_view(request):
    if request.method == 'POST':
        form = ReservationReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            status = form.cleaned_data.get('status')

            reservations = Reservation.objects.filter(
                check_in__gte=start_date,
                check_out__lte=end_date
            )
            if status:
                reservations = reservations.filter(status=status)

            headers = ['کد تأیید', 'رزروکننده', 'اتاق', 'از تاریخ', 'تا تاریخ', 'وضعیت', 'هزینه (تومان)']
            rows = []
            for r in reservations:
                rows.append([
                    r.confirmation_code,
                    f'{r.user.first_name} {r.user.last_name}',
                    r.room_type.name,
                    str(r.check_in),
                    str(r.check_out),
                    r.get_status_display(),
                    f'{r.room_type.price:,}',
                ])

            pdf_buffer = build_pdf_table(
                title=f'گزارش رزروها ({start_date} تا {end_date})',
                headers=headers,
                rows=rows,
            )

            logger.info(f'گزارش رزروها توسط {request.user.username} تولید شد.')
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reservations_report.pdf"'
            return response
    else:
        form = ReservationReportForm()

    return render(request, 'reservations/reservation_report_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def financial_report_view(request):
    if request.method == 'POST':
        form = FinancialReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            reservations = Reservation.objects.filter(
                status='checked_out',
                check_out__gte=start_date,
                check_out__lte=end_date,
            )

            headers = ['کد تأیید', 'اتاق', 'تاریخ تسویه', 'هزینه (تومان)']
            rows = []
            total = 0
            for r in reservations:
                price = r.room_type.price
                total += price
                rows.append([r.confirmation_code, r.room_type.name, str(r.check_out), f'{price:,}'])

            pdf_buffer = build_pdf_table(
                title=f'گزارش مالی ({start_date} تا {end_date})',
                headers=headers,
                rows=rows,
                footer_text=f'جمع کل: {total:,} تومان',
            )

            logger.info(f'گزارش مالی توسط {request.user.username} تولید شد.')
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="financial_report.pdf"'
            return response
    else:
        form = FinancialReportForm()

    return render(request, 'reservations/financial_report_form.html', {'form': form})