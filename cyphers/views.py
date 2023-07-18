from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from challenges.models import Challeng, CyphersUserChalleng
from users.models import CyphersUser
# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):  
    return render(request, 'about.html')

def profile(request):
    return render(request, 'profile.html')

def challenges(request):
    if request.method == 'POST':
        unblock_code = request.POST.get('unblock_code')
        pk = request.POST.get("pk")
        user_challeng = CyphersUserChalleng.objects.get(pk=pk)              
        if unblock_code == user_challeng.unblock_code:
            
            user_challeng.is_blocked = False
            user_challeng.is_active = True
            user_challeng.save()
    user_challenges = CyphersUserChalleng.objects.filter(user=request.user)
    return render(request, 'challenges.html', {'challenges': user_challenges})

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'logout.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
    
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active")

        else:
            print("Someone tried to login and failed!")
            print(f"Username: {username} and password {password}")
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request, 'login.html', {})
    return render(request, 'login.html')

def user_registration(request):
    registered = False

    if request.method == "POST":
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')

        if password_1 == password_2:
             user = CyphersUser(username = username, password = make_password(password_1))
             user.save()
             
             registered = True
        else:
            print("Password error")
    return render(request, "registration.html")
    
def play_challeng(request, user_challeng_pk):  
    user_challeng = CyphersUserChalleng.objects.get(pk = user_challeng_pk) 
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer == user_challeng.answer:
            user_challeng.is_active = False
            user_challeng.is_done = True
            user_challeng.save()
        return HttpResponseRedirect(reverse('challenges'))
    return render(request, 'play-challeng.html', {'user_challeng':user_challeng})