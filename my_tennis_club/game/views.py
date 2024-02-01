from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from record.models import PlayRecord
from leaderboard.models import Leaderboard
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

@login_required
def game_main(request):
    user = request.user
    return render(request, 'whack_hole.html', {'username': user.username})

def logout_view(request):
    logout(request)
    return JsonResponse({'alertMessage': '成功登出'})

@login_required
def start_game(request):
    user = request.user
    return render(request, 'game_main.html', {'username': user.username})

@login_required
def game_end(request):
    user = request.user
    username = user.username
    nowDate = datetime.now()

    if request.method == 'POST':
        # 使用 JSON 解析 POST 數據
        data = json.loads(request.body)
        score = data.get('score', 0)

        if score < 0:
            return JsonResponse({'error': 'Invalid score.'}, status=400)
        
        # 將分數保存到 PlayRecord 中
        PlayRecord.objects.create(username=username, score=score, date=nowDate)

        # 判斷是否超過 bestScore
        try:
            user_best = Leaderboard.objects.get(username=username)
            if score > user_best.bestscore:
                user_best.bestscore = score
                user_best.save()
        except Leaderboard.DoesNotExist:
            Leaderboard.objects.create(username=username, bestscore=score)

        return JsonResponse({'message': 'Score saved successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)