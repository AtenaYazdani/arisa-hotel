from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    content = models.TextField(verbose_name='متن خبر')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='نمایش در سایت')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')

    class Meta:
        verbose_name = 'خبر'
        verbose_name_plural = 'اخبار و رویدادها'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title