from django.db import models


class Hall(models.Model):
    FACILITY_TYPE_CHOICES = [
        ('restaurant', 'رستوران'),
        ('cafe', 'کافه'),
        ('massage', 'ماساژ'),
    ]
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPE_CHOICES, verbose_name='نوع')
    name = models.CharField(max_length=100, verbose_name='نام سالن')
    image = models.ImageField(upload_to='halls/', verbose_name='تصویر')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='ترتیب نمایش')
    class Meta:
        verbose_name = 'سالن'
        verbose_name_plural = 'سالن‌ها'
        ordering = ['order']
    def __str__(self):
        return f'{self.name} ({self.get_facility_type_display()})'