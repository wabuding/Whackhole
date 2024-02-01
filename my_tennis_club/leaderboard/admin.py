from django.contrib import admin
from .models import Leaderboard

class LeaderboardAdmin(admin.ModelAdmin):
  list_display = ("username", "bestscore",)
  
admin.site.register(Leaderboard, LeaderboardAdmin)