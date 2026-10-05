from django.db import models


class Category(models.Model):
    name_en = models.CharField(max_length=100, unique=True)
    name_fa = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='تصویر دسته‌بندی')
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'دسته‌بندی اتاق'
        verbose_name_plural = 'دسته‌بندی‌های اتاق'

    def __str__(self):
        return f'{self.name_en} ({self.name_fa})'