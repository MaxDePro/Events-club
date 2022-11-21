from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You success register')
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'authentication/register_user.html', context={'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You were logout!')
    return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Yo have failed to login, Try again')
            return redirect('login_page')
    else:
        return render(request, 'authentication/login.html', {})


