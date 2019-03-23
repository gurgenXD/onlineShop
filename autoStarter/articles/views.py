from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from articles.models import Article


def articles(request):
    articles = Article.objects.filter(published=True)

    PRODUCT_PER_PAGE = 8
    
    paginator = Paginator(articles, PRODUCT_PER_PAGE)
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
        'articles': articles,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'articles/articles.html', context)


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=int(article_id))

    context = {
        'article': article,
    }

    return render(request, 'article_detail/article_detail.html', context)

