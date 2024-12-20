from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Profile


# Login view
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("create_report")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "users/login.html")


# Registration view
def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            Profile.objects.create(user=user, username=user.username, email=user.email)
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
    return render(request, "users/register.html")


# Logout view
def user_logout(request):
    logout(request)
    return redirect("login")
