from django.shortcuts import render
from rooms.models import Category
from pages.models import News
from pages.models import GalleryImage

def index_view(request):
    categories = Category.objects.filter(is_active=True).prefetch_related('room_types')[:3]
    latest_news = News.objects.filter(is_active=True)[:4]
    gallery_images = GalleryImage.objects.all()[:7]


    return render(request, 'core/index.html', {
        'categories': categories,
        'latest_news': latest_news,
        'gallery_images': gallery_images,
    })
