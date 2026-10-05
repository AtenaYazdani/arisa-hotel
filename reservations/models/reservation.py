import random
from django.db import models
from accounts.models import User
from rooms.models import RoomType


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('confirmed', 'تأییدشده'),
        ('delivered', 'تحویل‌شده'),
        ('checked_out', 'تسویه‌شده'),
        ('cancelled', 'لغوشده'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name='کاربر')
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='reservations', verbose_name='نوع اتاق')
    check_in = models.DateField(verbose_name='تاریخ ورود')
    check_out = models.DateField(verbose_name='تاریخ خروج')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت رزرو')
    note = models.TextField(blank=True, verbose_name='توضیحات')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    confirmation_code = models.CharField(max_length=5, unique=True, editable=False, verbose_name='کد تأیید')
    class Meta:
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزروها'

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        while True:
            code = str(random.randint(10000, 99999))
            if not Reservation.objects.filter(confirmation_code=code).exists():
                return code

    @property
    def guests_count(self):
        return self.guests.count()

    def __str__(self):
        return f'{self.user} - {self.room_type} ({self.confirmation_code})'