from django.shortcuts import render
from pages.models import MassageService, Hall, PoolFeature

STATIC_PAGES = {}  # دیگر برای pool استفاده نمی‌شود، فقط اگر صفحه استاتیک دیگری بماند


def static_page_view(request, page_key):
    page = STATIC_PAGES[page_key]
    return render(request, 'pages/static_facility.html', page)


def pool_view(request):
    features = PoolFeature.objects.filter(is_active=True)
    return render(request, 'pages/pool.html', {'features': features})


def massage_view(request):
    services = MassageService.objects.filter(is_active=True)
    halls = Hall.objects.filter(facility_type='massage')
    return render(request, 'pages/massage.html', {'services': services, 'halls': halls})