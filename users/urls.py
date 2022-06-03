from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'users'
urlpatterns = [
    path('a/', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('login_user/', views.login_user_view, name='login_user'),
    path('register/', views.register_user, name='register'),
    path('log_out/', views.logout_view, name='goodbye'),
    path('b_view/', views.b_view, name='b_view'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
