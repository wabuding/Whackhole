from django.shortcuts import render
from record.models import PlayRecord
from django.contrib.auth.decorators import login_required

@login_required
def show_record(request):
    user_record = PlayRecord.objects.filter(username=request.user.username)
    return render(request, 'play_record.html', {'user_record': user_record})