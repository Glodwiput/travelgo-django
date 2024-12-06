from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User  
from django.contrib.auth.hashers import make_password

def register_view(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST.get('role', 'customer')  

        
        if password != confirm_password:
            messages.error(request, "Password dan konfirmasi password tidak cocok.")
            return render(request, 'users/register.html')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return render(request, 'users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah digunakan.")
            return render(request, 'users/register.html')

        
        user = User(
            username=username,
            email=email,
            role=role,
            password=make_password(password) 
        )
        user.save()

        
        new_user = authenticate(username=username, password=password)
        if new_user is not None:
            login(request, new_user)
            messages.success(request, "Pendaftaran berhasil! Anda telah login.")
            return redirect('login')  

    return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Username: {username}, Password: {password}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'customer':
                return redirect('home') 
            elif user.role == 'staff':
                return redirect('home') 
            elif user.role == 'admin':
                return redirect('home') 
        else:
            messages.error(request, "Username atau password salah.")
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'users/home.html')