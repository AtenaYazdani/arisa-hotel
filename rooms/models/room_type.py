import random
from django.db import models
from .category import Category
from .amenity import Amenity


class RoomType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='room_types', verbose_name='دسته‌بندی')
    name = models.CharField(max_length=100, verbose_name='نام اتاق')
    code = models.CharField(max_length=4, unique=True, editable=False, verbose_name='کد اتاق')

    description = models.TextField(blank=True, verbose_name='توضیحات')
    features = models.TextField(blank=True, help_text='هر ویژگی را در یک خط بنویسید', verbose_name='ویژگی‌های اتاق')

    price = models.PositiveIntegerField(verbose_name='قیمت هر شب (تومان)')
    quantity = models.PositiveSmallIntegerField(default=2, verbose_name='موجودی')

    capacity_label = models.CharField(max_length=50, blank=True, verbose_name='ظرفیت (متنی)')
    size_sqm = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='متراژ (متر مربع)')
    bed_type = models.CharField(max_length=100, blank=True, verbose_name='نوع تخت')
    view_type = models.CharField(max_length=100, blank=True, verbose_name='نوع چشم‌انداز')

    amenities = models.ManyToManyField(Amenity, blank=True, related_name='room_types', verbose_name='امکانات')

    is_active = models.BooleanField(default=True, verbose_name='نمایش در سایت')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'نوع اتاق'
        verbose_name_plural = 'انواع اتاق'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        while True:
            code = str(random.randint(1000, 9999))
            if not RoomType.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return f'{self.name} ({self.code})'