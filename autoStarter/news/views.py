from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from news.models import News


def news(request):
    all_news = get_list_or_404(News, published=True)

    PRODUCT_PER_PAGE = 8
    
    paginator = Paginator(all_news, PRODUCT_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page=%s' % page.previous_page_number()
    else:
        prev_url = '' 
    
    if page.has_next():
        next_url = '?page=%s' % page.next_page_number()
    else:
        next_url = '' 

    context = {
        'all_news': all_news,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'news/news.html', context)


def news_detail(request, news_id):
    one_news = get_object_or_404(News, id=int(news_id))

    context = {
        'one_news': one_news,
    }

    return render(request, 'news/news_detail.html', context)

