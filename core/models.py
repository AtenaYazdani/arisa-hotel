from django.db import models


class OTPCode(models.Model):
    PURPOSE_CHOICES = [
        ('register', 'ثبت‌نام'),
        ('login', 'ورود'),
    ]

    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    code = models.CharField(max_length=6, verbose_name='کد تأیید')
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, verbose_name='هدف')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    expires_at = models.DateTimeField(verbose_name='زمان انقضا')
    is_used = models.BooleanField(default=False, verbose_name='استفاده شده')

    class Meta:
        verbose_name = 'کد تأیید'
        verbose_name_plural = 'کدهای تأیید'

    def __str__(self):
        return f'{self.phone} - {self.code} ({self.get_purpose_display()})'
