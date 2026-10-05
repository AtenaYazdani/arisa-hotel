from django.urls import path
from core.views.index import index_view

app_name = 'core'

urlpatterns = [
    path('', index_view, name='index'),
]