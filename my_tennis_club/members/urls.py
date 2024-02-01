from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('register', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('register_check/', views.register_view, name='register_view'),
]