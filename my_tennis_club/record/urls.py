from django.urls import path
from . import views

app_name = 'record_url'

urlpatterns = [
    path('', views.show_record, name='show_record'),
]