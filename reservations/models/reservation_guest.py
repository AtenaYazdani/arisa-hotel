from django.db import models
from .reservation import Reservation


class ReservationGuest(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='guests', verbose_name='رزرو')
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')

    class Meta:
        verbose_name = 'مهمان رزرو'
        verbose_name_plural = 'مهمانان رزرو'

    def __str__(self):
        return f'{self.full_name} ({self.reservation.confirmation_code})'