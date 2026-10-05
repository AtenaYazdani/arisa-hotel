from django.shortcuts import render
from rooms.models import Category


def room_list_view(request):
    categories = Category.objects.filter(is_active=True).prefetch_related('room_types')
    return render(request, 'rooms/room_list.html', {'categories': categories})