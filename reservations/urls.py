from django.urls import path
from reservations.views.create_reservation import create_reservation_view
from reservations.views.my_reservations import my_reservations_view
from reservations.views.reports import reservation_report_view, financial_report_view

app_name = 'reservations'

urlpatterns = [
    path('book/<int:room_type_id>/', create_reservation_view, name='create'),
    path('my-reservations/', my_reservations_view, name='my_reservations'),
    path('reports/reservations/', reservation_report_view, name='reservation_report'),
    path('reports/financial/', financial_report_view, name='financial_report'),
]