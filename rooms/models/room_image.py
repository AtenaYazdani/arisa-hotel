from django.db import models
from .room_type import RoomType


class RoomImage(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='images', verbose_name='نوع اتاق')
    image = models.ImageField(upload_to='rooms/', verbose_name='تصویر')
    is_main = models.BooleanField(default=False, verbose_name='تصویر اصلی')

    class Meta:
        verbose_name = 'تصویر اتاق'
        verbose_name_plural = 'تصاویر اتاق'

    def __str__(self):
        return f'تصویر {self.room_type.name}'