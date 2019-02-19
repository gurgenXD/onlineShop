from shop.models import Category


def getting_categories(request):
	categories = Category.objects.all()

	context = {
		'categories': categories,
	}

	return context