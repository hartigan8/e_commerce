
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from . import models


from django.shortcuts import render, redirect
from . import CustomUserCreationForm
import joblib
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
model = joblib.load('final_xgb_model.pkl')
sia = SentimentIntensityAnalyzer()
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
    product_forms = {product.id: CommentForm() for product in products}
    return render(request, 'home.html', {'products': products, 'product_forms': product_forms})



from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .comment_form import CommentForm  # Import your CommentForm

def add_comment(request, product_id):
    product = get_object_or_404(models.Product, pk=product_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.recommended = is_recommended(comment)
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()

    return redirect('home')  # Redirect back to the home page

def is_recommended(comment):
    comment_text=comment.comment
    scores = sia.polarity_scores(comment_text)
    threshold = 0.5
    is_positive = scores['compound'] >= 0.1
    
    return is_positive