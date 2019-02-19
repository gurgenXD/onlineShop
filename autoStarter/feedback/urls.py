from django.urls import path
from feedback import views
from profiles.decorators import check_recaptcha


urlpatterns = [
    path('', check_recaptcha(views.feedback), name='feedback'),
]
