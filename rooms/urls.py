from django.urls import path
from rooms.views.room_list import room_list_view
from rooms.views.category_rooms import category_rooms_view
from rooms.views.room_detail import room_detail_view

app_name = 'rooms'

urlpatterns = [
    path('', room_list_view, name='list'),
    path('category/<int:category_id>/', category_rooms_view, name='category'),
    path('<int:room_id>/', room_detail_view, name='detail'),
]