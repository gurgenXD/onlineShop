from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from shop.models import Category, SubCategory, Product, Image, CarBrand, Car, CarModel, Manufacturer
from orders.cart import Cart


def catalog(request):
    return render(request, 'shop/catalog.html', {})


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = get_list_or_404(SubCategory, category=category)

    context = {
        'category': category,
        'subcategories': subcategories,
    }

    return render(request, 'shop/category.html', context)


def subcategory(request, category_slug, subcategory_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
    
    cars_brands = get_list_or_404(CarBrand)

    car_brand_id = request.GET.get('cars-brand')
    car_model_id = request.GET.get('cars-name')
    car_id = request.GET.get('cars-date')

    if car_brand_id:
        car_brand = get_object_or_404(CarBrand, id=int(car_brand_id))
        cars_models = get_list_or_404(CarModel, brand=car_brand)
        cars = get_list_or_404(Car, brand=car_brand)
        cars_for_filter = cars
        if car_model_id:
            car_model = get_object_or_404(CarModel, id=int(car_model_id))
            cars = get_list_or_404(Car, brand=car_brand, car_model=car_model)
            cars_for_filter = cars
            if car_id:
                car = get_object_or_404(Car, id=int(car_id))
                release_date = car.release_date
                cars_for_filter= [car]
            else:
                release_date = None
        else:
            release_date = None
            car_model = None
    else:
        cars = None
        car_brand = None
        cars_models = None
        car_model = None
        release_date = None
        cars_for_filter = get_list_or_404(Car)

    sort_products = request.GET.get('sort-products')
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)

    if sort_products == '1':
        products = get_list_or_404(Product.objects.order_by('-purchased').distinct(), subcategory=subcategory, cars__in=cars_for_filter,  is_active=True)
    elif sort_products == '2':
        products = get_list_or_404(Product.objects.order_by('price').distinct(), subcategory=subcategory, cars__in=cars_for_filter, is_active=True)
    elif sort_products == '3':
        products = get_list_or_404(Product.objects.order_by('-price').distinct(), subcategory=subcategory, cars__in=cars_for_filter, is_active=True)
    else:
        products = get_list_or_404(Product.objects.order_by('-purchased').distinct(), subcategory=subcategory, cars__in=cars_for_filter, is_active=True)
    
    products_prices = [product.price for product in products]

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        min_price = int(min_price)
        products = [product for product in products if product.price>=int(min_price)]
    else:
        min_price = min(products_prices)
    
    if max_price:
        max_price = int(max_price)
        products = [product for product in products if product.price<=int(max_price)]
    else:
        max_price = max(products_prices)

    manufacturers = get_list_or_404(Manufacturer)
    manuf_checked = [manufacturer for manufacturer in manufacturers if manufacturer.slug in request.GET]
    if len(manuf_checked) != 0:
        products = [product for product in products if product.manufacturer in manuf_checked]
        
    products_len = len(products)

    PRODUCT_PER_PAGE = 10
    paginator = Paginator(products, PRODUCT_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    is_paginated = page.has_other_pages()

    request_get_string = '?'
    for request_get_keys in request.GET.keys():
        request_get_string += request_get_keys + '=' + request.GET.get(request_get_keys) + '&'
    request_get_string = request_get_string[:-1]
    
    if page.has_previous():
        prev_url = request_get_string + '&page=%s' % page.previous_page_number()
    else:
        prev_url = '' 
    
    if page.has_next():
        next_url = request_get_string + '&page=%s' % page.next_page_number()
    else:
        next_url = '' 

    context = {
        'category': category,
        'subcategory': subcategory,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'cars_brands': cars_brands,
        'car_brand': car_brand,
        'cars_models': cars_models,
        'car_model': car_model,
        'cars': cars,
        'min_price': min_price,
        'max_price': max_price,
        'release_date': release_date,
        'manufacturers': manufacturers,
        'manuf_checked': manuf_checked,
        'products_len': products_len,
        'sort_products': sort_products,
        'request_get_string': request_get_string,
    }

    return render(request, 'shop/subcategory.html', context)


def product(request, category_slug, subcategory_slug, product_slug):
    cart = Cart(request)
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    images = get_list_or_404(Image, product=product)
    cars = Car.objects.filter(products__in=[product])
    similar = Product.objects.filter(is_active=True)
    similar = similar.filter(Q(cars__in=cars)|Q(subcategory=subcategory)|Q(category=category)).distinct()
    similar = similar.exclude(name=product.name)
    if len(similar) > 8:
        similar = similar[:8]

    if str(product.id) in cart.cart:
        product_in_cart = True
    else:
        product_in_cart = False

    context = {
        'category': category,
        'subcategory': subcategory,
        'product': product,
        'images': images,
        'product_in_cart': product_in_cart,
        'similar': similar,
    }

    return render(request, 'shop/product_detail.html', context)


def search_products(request):
    products = Product.objects.filter(is_active=True)
    query = request.GET.get('query')

    if query:
        products = products.filter(
            Q(name__icontains=query)|
            Q(category__name__icontains=query)|
            Q(subcategory__name__icontains=query)|
            Q(manufacturer__name__icontains=query)|
            Q(description__icontains=query)|
            Q(cars__car_model__name__icontains=query)|
            Q(cars__brand__name__icontains=query)
            ).order_by('-purchased').distinct()
    
    products_len = len(products)

    PRODUCT_PER_PAGE = 10
    
    paginator = Paginator(products, PRODUCT_PER_PAGE)
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
        'products_len': products_len,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }
    return render(request, 'shop/search_products.html', context)