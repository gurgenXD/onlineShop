from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from orders.cart import Cart
from orders.dandp import DandP
from shop.models import Product, Category
from orders.forms import OrderForm
from orders.models import OrderItem, Order, Delivery, Payment, StatusDelivery, StatusPayment
from static_strings.models import MailToString


def add(request):
    cart = Cart(request)
    product_id = int(request.GET.get('product_id'))
    qty = int(request.GET.get('qty'))
    product = Product.objects.get(id=product_id)
    cart.add(product, qty)

    context = {
        'cart_len': len(cart),
        'total_price': cart.get_total_price(),
    }
    return JsonResponse(context)


def remove(request):
    cart = Cart(request)
    product_id = int(request.GET.get('product_id'))
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    
    context = {
        'cart_len': len(cart),
        'total_price': cart.get_total_price(),
    }

    return JsonResponse(context)


def change_quantity(request):
    cart = Cart(request)
    product_id = int(request.GET.get('product_id'))
    product = Product.objects.get(id=product_id)
    quantity = int(request.GET.get('quantity'))
    cart.change_quantity(product=product, quantity=quantity)

    cost = int(cart.cart[str(product.id)]['cost'])

    context = {
        'cart_len': len(cart),
        'total_price': cart.get_total_price(),
        'cost': cost,
    }

    return JsonResponse(context)


def cart(request):
    delivery_address = Delivery.objects.get(id=1).address

    dandp = DandP(request)

    delivery = int(dandp.dandp['delivery'])
    payment = int(dandp.dandp['payment'])

    context = {
        'delivery': delivery,
        'payment': payment,
        'delivery_address': delivery_address,
    }

    return render(request, 'orders/cart.html', context)


@login_required
def contact_info(request):
    cart = Cart(request)
    if len(cart) != 0:
        if request.method == 'POST':
            dandp = DandP(request)
            delivery = request.POST.get('delivery')
            payment = request.POST.get('payment')

            if delivery == 0:
                dandp.dandp['delivery'] = 0
            if delivery == 1:
                dandp.dandp['delivery'] = 1
            if payment == 0:
                dandp.dandp['payment'] = 0
            if payment == 1:
                dandp.dandp['payment'] = 1

            dandp.update(delivery, payment)
    else:
        return redirect('cart')

    form = OrderForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'orders/contact_info.html', context)


@login_required
def order(request):
    if request.method == 'POST':
        user = request.user
        form = OrderForm(user, request.POST)
        if form.is_valid():
            user.profile.full_name = form.cleaned_data['full_name']
            user.profile.phone = form.cleaned_data['phone']
            user.profile.postcode = form.cleaned_data['postcode']
            user.profile.region = form.cleaned_data['region']
            user.profile.locality = form.cleaned_data['locality']
            user.profile.street = form.cleaned_data['street']
            user.profile.house_nmb = form.cleaned_data['house_nmb']
            user.profile.apartment_nmb = form.cleaned_data['apartment_nmb']
            user.save()
    else:
        return redirect('cart')

    dandp = DandP(request)
    delivery_id = int(dandp.dandp['delivery']) + 1
    payment_id = int(dandp.dandp['payment']) + 1

    delivery = Delivery.objects.get(id=delivery_id)
    payment = Payment.objects.get(id=payment_id)

    context = {
        'delivery': delivery,
        'payment': payment,
    }

    return render(request, 'orders/order.html', context)


@login_required
def order_submit(request):
    user = request.user
    cart = Cart(request)
    if len(cart) != 0:
        dandp = DandP(request)
        delivery = Delivery.objects.get(id=int(dandp.dandp['delivery'])+1)
        payment = Payment.objects.get(id=int(dandp.dandp['payment'])+1)
        status_delivery = StatusDelivery.objects.get(id=1)
        status_payment = StatusPayment.objects.get(id=1)

        order = Order.objects.create(
            user = user.profile,
            email = user.email,
            total_price = cart.get_total_price(),
            delivery = delivery,
            status_delivery = status_delivery,
            payment = payment,
            status_payment = status_payment,
            full_name = user.profile.full_name,
            phone = user.profile.phone,
            postcode = user.profile.postcode,
            region = user.profile.region,
            locality = user.profile.locality,
            street = user.profile.street,
            house_nmb = user.profile.house_nmb,
            apartment_nmb = user.profile.apartment_nmb
        )

        for item in cart:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(order=order, product=product, price=item['price'], quantity=item['quantity'], total_price=item['cost'])

            product.save()

        cart.clear()
        dandp.clear()

        current_site = get_current_site(request)
        mail_subject = 'Новый заказ на сайте: ' + current_site.domain
        message = render_to_string('orders/order_submit_message.html', {
            'domain': current_site.domain,
            'order': order,
        })
        to_email = MailToString.objects.all().first().email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        
        context = {}
        return render(request, 'orders/order_submit.html', context)
    else:
        return redirect('cart')


def order_one_click(request):
    product_id = int(request.GET.get('product_id'))
    quantity = int(request.GET.get('quantity'))
    product = Product.objects.get(id=product_id)

    status_delivery = StatusDelivery.objects.get(id=1)
    status_payment = StatusPayment.objects.get(id=1)

    price = product.price
    total_price = quantity * price

    order = Order.objects.create(
        total_price = total_price,
        full_name = request.GET.get('user_name'),
        phone = request.GET.get('user_phone'),
        comment = request.GET.get('user_comment'),
        status_delivery = status_delivery,
        status_payment = status_payment,
    )

    orderitem = OrderItem.objects.create(
        order=order,
        product=product,
        price=price,
        quantity=quantity,
        total_price=total_price
    )
    
    product.save()

    try:
        alert_success = True
        current_site = get_current_site(request)
        mail_subject = 'Новый заказ на сайте: ' + current_site.domain
        message = render_to_string('orders/order_submit_message.html', {
            'domain': current_site.domain,
            'order': order,
        })
        to_email = MailToString.objects.all().first().email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except:
        alert_success = False

    context = {
        'alert_success': alert_success,
    }
    return JsonResponse(context)