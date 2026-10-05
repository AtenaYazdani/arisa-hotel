from django.db import models


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/', verbose_name='تصویر')
    place_name = models.CharField(max_length=100, verbose_name='نام مکان')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='ترتیب')

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری'
        ordering = ['order']