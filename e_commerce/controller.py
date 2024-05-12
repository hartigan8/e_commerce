
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from . import models


from django.shortcuts import render, redirect
from . import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            auth_login(request, user)  # Log in the newly created user
            return redirect('home')  # Redirect to the home page or another appropriate page
        else:
            # If the form is not valid, render the page again with form errors
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm.CustomUserCreationForm()  # Instantiate a new form for a GET request

    return render(request, 'register.html', {'form': form})


        

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'login_error': 'Invalid credentials'})
    return render(request, 'login.html')

def home(request):
    products = models.Product.objects.all()

    return render(request, 'home.html', {'products': products})

