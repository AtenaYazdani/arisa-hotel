from django.db import models


class PoolFeature(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='pool/', verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='نمایش در سایت')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'ویژگی استخر'
        verbose_name_plural = 'استخر (ویژگی‌ها)'
        ordering = ['order']

    def __str__(self):
        return self.name