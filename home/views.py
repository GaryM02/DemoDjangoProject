from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# homepage for if user is unauthenticated
def unauthhome(request):
    return render(request, "home/unauthhome.html", {})


# Create your views here.
@login_required(login_url='login')
def home(response):
    return render(response, "home/home.html", {})

def contact(response):
    return render(response, "home/contact.html", {})

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('authorisedhome')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('authorisedhome')
            else:
                messages.info(request, 'Username Or Password Is Incorrect!')
                
        return render(request, "home/login.html", {})

def logoutuser(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('authorisedhome')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {user}')
                return redirect('login')

        return render(request, "home/register.html", {'form':form})
