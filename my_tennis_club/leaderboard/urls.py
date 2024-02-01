from django.urls import path
from . import views

app_name = 'leaderboard_url'

urlpatterns = [
    path('', views.show_leader, name='show_leader'),
]