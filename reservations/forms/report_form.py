from django import forms
from reservations.models import Reservation


class ReservationReportForm(forms.Form):
    start_date = forms.DateField(
        label='از تاریخ',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label='تا تاریخ',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    status = forms.ChoiceField(
        label='وضعیت',
        choices=[('', 'همه')] + Reservation.STATUS_CHOICES,
        required=False,
    )
class FinancialReportForm(forms.Form):
    start_date = forms.DateField(
        label='از تاریخ',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label='تا تاریخ',
        widget=forms.DateInput(attrs={'type': 'date'})
    )