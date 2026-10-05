from django.shortcuts import render, get_object_or_404
from rooms.models import RoomType


def room_detail_view(request, room_id):
    room = get_object_or_404(RoomType, id=room_id, is_active=True)
    images = list(room.images.all()[:3])
    # پر کردن جای خالی تا همیشه ۳ خانه داشته باشیم (بدون نشون‌دادن خالی‌بودن)
    while len(images) < 3:
        images.append(None)

    return render(request, 'rooms/room_detail.html', {
        'room': room,
        'images': images,
    })