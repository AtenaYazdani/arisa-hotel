from django.db import models


class Amenity(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام امکان')
    icon = models.ImageField(upload_to='amenities/', blank=True, null=True, verbose_name='آیکون')

    class Meta:
        verbose_name = 'امکان اتاق'
        verbose_name_plural = 'امکانات اتاق'

    def __str__(self):
        return self.name