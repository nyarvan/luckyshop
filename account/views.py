from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, logout


def registration_view(request):
    form = UserRegistrationForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('shop:homepage')
    return render(request, 'register.html', context={
        'form': form,
    })


def login_view(request):
    form = UserLoginForm(data=request.POST or None)

    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('shop:homepage')

    return render(request, 'login.html', context={
        'form': form,
    })


def logout_view(request):
    logout(request)
    return redirect('shop:homepage')
