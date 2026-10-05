from django.contrib import admin
from pages.models import News, Hall, MenuItem
from pages.models import MassageService
from pages.models import GalleryImage
from pages.models import PoolFeature


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title',)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'order')
    list_filter = ('facility_type',)
    list_editable = ('order',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'price', 'order')
    list_filter = ('facility_type',)
    list_editable = ('order',)
    search_fields = ('name',)

@admin.register(MassageService)
class MassageServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('place_name', 'order')
    list_editable = ('order',)


@admin.register(PoolFeature)
class PoolFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)