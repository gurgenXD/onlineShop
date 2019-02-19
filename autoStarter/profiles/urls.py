from django.urls import path
from profiles import views
from profiles.decorators import check_recaptcha


urlpatterns = [
    path('signin/', check_recaptcha(views.signin), name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('profile/info/', views.profile, name='profile'),
    path('profile/orders/', views.orders, name='orders'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password-reset/', check_recaptcha(views.PasswordReset.as_view()), name='password_reset'),
    path('password-reset-done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password-reset-complete', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]