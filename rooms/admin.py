from django.contrib import admin
from rooms.models import Category, Amenity, RoomType, RoomImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_fa', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name_en', 'name_fa')


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'price', 'quantity', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code')
    readonly_fields = ('code',)
    filter_horizontal = ('amenities',)
    inlines = [RoomImageInline]

    fieldsets = (
        (None, {'fields': ('category', 'name', 'code', 'is_active')}),
        ('توضیحات', {'fields': ('description', 'features')}),
        ('قیمت و موجودی', {'fields': ('price', 'quantity')}),
        ('مشخصات فیزیکی', {'fields': ('capacity_label', 'size_sqm', 'bed_type', 'view_type')}),
        ('امکانات', {'fields': ('amenities',)}),
    )