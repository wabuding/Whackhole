from django.urls import path
from . import views

app_name = 'games_url'

urlpatterns = [
    path('', views.game_main, name='whackhole'),
    path('logout/', views.logout_view, name='logout_view'),
    path('whackhole/gamestart/', views.start_game, name='game_start'),
    path('whackhole/gameend', views.game_end, name='game_end'),
]