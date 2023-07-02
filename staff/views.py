from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import UserForm

# Create your views here.
def login_staff(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, ('Successfully logged in'))
            return HttpResponseRedirect(reverse('app:index'))
        
        else:
            messages.success(request, ('Error logging in, please try again'))
            return HttpResponseRedirect(reverse('staff:login'))
    
    else:
        return render(request, 'staff/login.html', {
        
    })

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:index'))

def register_staff(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, ('Successfully registered account, please login'))
    
        else:
            print(user_form.errors)
            messages.success(request, ('Registration failed, please try again'))

        return redirect('staff:login')

    
    else:
        user_form = UserCreationForm()
        return render(request, 'staff/registration.html', {
            'user_form': user_form,

        })