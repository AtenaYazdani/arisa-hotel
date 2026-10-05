from django.db import models


class MassageService(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام خدمت')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='massage/', verbose_name='تصویر')
    duration_minutes = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='مدت زمان (دقیقه)')
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت (تومان)')
    is_active = models.BooleanField(default=True, verbose_name='نمایش در سایت')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'خدمت ماساژ'
        verbose_name_plural = 'خدمات ماساژ'
        ordering = ['order']

    def __str__(self):
        return self.name