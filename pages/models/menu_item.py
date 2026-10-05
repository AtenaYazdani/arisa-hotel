from django.db import models


class MenuItem(models.Model):
    FACILITY_TYPE_CHOICES = [
        ('restaurant', 'رستوران'),
        ('cafe', 'کافه'),
    ]
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPE_CHOICES, verbose_name='نوع')
    name = models.CharField(max_length=100, verbose_name='نام آیتم')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    price = models.PositiveIntegerField(verbose_name='قیمت (تومان)')
    image = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='نمایش در سایت')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'آیتم منو'
        verbose_name_plural = 'آیتم‌های منو'
        ordering = ['order']
    def __str__(self):
        return f'{self.name} ({self.get_facility_type_display()})'