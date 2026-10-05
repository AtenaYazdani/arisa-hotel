from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rooms.models import Category, RoomType


def category_rooms_view(request, category_id):
    category = get_object_or_404(Category, id=category_id, is_active=True)
    rooms = RoomType.objects.filter(category=category, is_active=True)

    query = request.GET.get('q', '').strip()
    if query:
        rooms = rooms.filter(Q(name__icontains=query) | Q(view_type__icontains=query))

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        rooms = rooms.order_by('price')
    elif sort == 'price_desc':
        rooms = rooms.order_by('-price')

    return render(request, 'rooms/category_rooms.html', {
        'category': category,
        'rooms': rooms,
        'current_sort': sort,
        'query': query,
    })