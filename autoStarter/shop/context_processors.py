from shop.models import Category, Product


def getting_categories(request):
	categories = Category.objects.all()

	context = {
		'categories': categories,
	}

	return context