
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return HttpResponse("You are successfully logged in")
            return redirect('dashboard')
        else:
            # Return an error message if authentication fails
            messages.error(request, 'Invalid username or password.')
            return HttpResponse("Wrong Details")
    return render(request, 'login.html')  # Render the login form template


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))