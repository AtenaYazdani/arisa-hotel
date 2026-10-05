from django.db import models
from accounts.models import User


class AdminMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='فرستنده')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='گیرنده')
    text = models.TextField(verbose_name='متن پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')

    class Meta:
        verbose_name = 'پیام ادمین'
        verbose_name_plural = 'پیام‌های ادمین'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender} → {self.receiver}: {self.text[:30]}'

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')

    class Meta:
        verbose_name = 'مشترک خبرنامه'
        verbose_name_plural = 'اطلاع‌رسانی (خبرنامه)'

    def __str__(self):
        return self.email