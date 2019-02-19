from shop.models import Product
from django.forms.models import model_to_dict


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': qty,
                                     'price': product.price,
                                     'cost': product.price * qty}
        self.save()

    def change_quantity(self, product, quantity):
        self.cart[str(product.id)]['quantity'] = quantity
        self.cart[str(product.id)]['cost'] = product.price * quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product_name'] = product.name
            self.cart[str(product.id)]['product_get_absolute_url'] = product.get_absolute_url()
            self.cart[str(product.id)]['product_id'] = product.id
            self.cart[str(product.id)]['product_stock'] = product.stock
            self.cart[str(product.id)]['product_image_url'] = product.get_main_image().image.url

        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['quantity'] = int(item['quantity'])
            item['cost'] = int(item['cost'])
            yield item

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_price(self):
        return sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.session.modified = True
