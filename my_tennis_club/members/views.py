from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
import json

def login_page(request):
    logout(request)
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            request.session['user_username'] = user.username
            request.session['user_password'] = user.password

            return JsonResponse({'alertMessage': '登入成功'})
        else:
            return JsonResponse({'alertMessage': '登入失敗'})

    return JsonResponse({'alertMessage': '登入失敗'})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return JsonResponse({'alertMessage': '建立成功'})
        else:
            errors = {field: form.errors[field][0] for field in form.errors}
            error_message = json.dumps(errors)
            error_message = error_message.replace("{", " ").replace("}", " ").replace('"', ' ')
            error_message = error_message.replace(' password2 :  The two password fields didn\\u2019t match. ', '再次輸入密碼與密碼不同')
            error_message = error_message.replace(' username :  A user with that username already exists. ', '使用者名稱已存在')
            error_message = error_message.replace(' password2 :  This password is too common. ', '密碼太過普通')
            error_message = error_message.replace(' password2 :  This password is too short. It must contain at least 8 characters. ', '密碼至少8個字')
            return JsonResponse({'alertMessage': error_message})

    return JsonResponse({'alertMessage': '建立失敗'})