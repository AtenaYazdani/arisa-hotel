from django.shortcuts import render
from django.db.models import Q
from pages.models import Hall, MenuItem

MENU_PAGES = {
    'restaurant': {
        'title': 'رستوران‌های آریسا',
        'eyebrow': 'تجربه‌ای فراتر از طعم',
        'description': 'در رستوران‌های آریسا، هر وعده غذایی ترکیبی از هنر آشپزی، مواد اولیه درجه یک و فضایی برای لحظاتی به‌یادماندنی است.',
        'hero_image': 'images/pages/restaurant-hero.jpg',
        'promo_title': 'طعمی به‌یادماندنی، تجربه‌ای بی‌نظیر',
        'promo_text': 'با رزرو میز از پیش، از منوهای ویژه و پیشنهادهای اختصاصی آریسا بهره‌مند شوید.',
    },
    'cafe': {
        'title': 'کافه‌ای برای لحظه‌های خاص شما',
        'eyebrow': 'تجربه‌ای فراتر از عادی',
        'description': 'در فضایی دنج و لوکس، از عطر قهوه‌های تخصصی و طعم دل‌نشین دسرهای دست‌ساز لذت ببرید.',
        'hero_image': 'images/pages/cafe-hero.jpg',
        'promo_title': 'لحظه‌ای برای خودتان',
        'promo_text': 'با سفارش ترکیبی از منوی کافه، از تخفیف‌های ویژه آریسا بهره‌مند شوید.',
    },
}


def menu_page_view(request, facility_type):
    meta = MENU_PAGES[facility_type]
    halls = Hall.objects.filter(facility_type=facility_type)
    menu_items = MenuItem.objects.filter(facility_type=facility_type)

    query = request.GET.get('q', '').strip()
    if query:
        menu_items = menu_items.filter(name__icontains=query)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        menu_items = menu_items.order_by('price')
    elif sort == 'price_desc':
        menu_items = menu_items.order_by('-price')

    return render(request, 'pages/menu_page.html', {
        'page_title': meta['title'],
        'eyebrow': meta['eyebrow'],
        'description': meta['description'],
        'hero_image': meta['hero_image'],
        'promo_title': meta['promo_title'],
        'promo_text': meta['promo_text'],
        'halls': halls,
        'menu_items': menu_items,
        'query': query,
        'current_sort': sort,
    })