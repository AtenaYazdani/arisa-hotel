from django.urls import path
from pages.views.static_pages import static_page_view, pool_view, massage_view
from pages.views.menu_pages import menu_page_view
from pages.views.news_list import news_list_view

app_name = 'pages'

urlpatterns = [
    path('pool/', pool_view, name='pool'),
    path('massage/', massage_view, name='massage'),
    path('restaurant/', menu_page_view, {'facility_type': 'restaurant'}, name='restaurant'),
    path('cafe/', menu_page_view, {'facility_type': 'cafe'}, name='cafe'),
    path('news/', news_list_view, name='news_list'),
]