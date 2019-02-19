from orders.cart import Cart


def getting_cartinfo(request):
	cart = Cart(request)
	cart_len = len(cart)

	for item in cart.cart.values():
		item['cost'] = int(item['cost'])

	context = {
		'cart': cart,
		'cart_len': cart_len,
	}

	return context