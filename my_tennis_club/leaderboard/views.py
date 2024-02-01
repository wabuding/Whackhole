from django.shortcuts import render
from leaderboard.models import Leaderboard
from django.db.models import F, Window
from django.db.models.functions import Rank
from django.contrib.auth.decorators import login_required

# 顯示排行
@login_required
def show_leader(request):
    user = request.user
    all_leader = Leaderboard.objects.annotate(rank=Window(expression=Rank(), order_by=F('bestscore').desc()))
    return render(request, 'leaderboard.html', {'all_leader': all_leader, 'username': user.username})