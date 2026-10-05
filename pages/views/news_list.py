from django.shortcuts import render
from pages.models import News


def news_list_view(request):
    news_items = News.objects.filter(is_active=True)
    return render(request, 'pages/news_list.html', {'news_items': news_items})