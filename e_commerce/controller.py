from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from . import models
from . import CustomUserCreationForm
from .comment_form import CommentForm  # Import your CommentForm
import joblib
from scipy.sparse import csr_matrix
import pandas as pd
# Load the TF-IDF vectorizer and XGBoost model
tfidf_vectorizer = joblib.load('./tfidf_vectorizer.pkl')
model = joblib.load('./final_xgb_model.pkl')
nb = joblib.load("./nb.pkl")
log = joblib.load("./log.pkl")
svc = joblib.load("./svc.pkl")
rf = joblib.load("./rf.pkl")

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

def add_comment(request, product_id):
    product = get_object_or_404(models.Product, pk=product_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.recommended = is_recommended(comment, request.user, product)
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()

    return redirect('home')  # Redirect back to the home page


def is_recommended(comment, user, product):
    # Extract the features
    comment_text = comment.comment
    rating = comment.rating
    positive_feedback_count = 0  # Set default or fetch actual value if available
    cluster = 0  # Set default or fetch actual value if available
    age_group = 0  # Set default or fetch actual value if available

    # One-hot encode categorical features as used during training
    division_name = product.division_name
    department_name = product.department_name
    class_name = product.class_name

    # Transform the comment text using the TF-IDF vectorizer
    comment_tfidf = tfidf_vectorizer.transform([comment_text])
    
    # Create predictions from other models
    nb_pred = nb.predict(comment_tfidf)[0]
    log_pred = log.predict(comment_tfidf)[0]
    svc_pred = svc.predict(comment_tfidf)[0]
    rf_pred = rf.predict(comment_tfidf)[0]
    
    # Create a DataFrame for other features
    features_dict = {
        'Rating': [rating],
        'Positive Feedback Count': [positive_feedback_count],
        'Cluster': [cluster],
        'Age_Group': [age_group],
        'nb_pred': [nb_pred],
        'log_pred': [log_pred],
        'svc_pred': [svc_pred],
        'rf_pred': [rf_pred]
    }
    
    # One-hot encode categorical features
    possible_divisions = ['General', 'General Petite', 'Intimates']
    possible_departments = ['Bottoms', 'Dresses', 'Intimate', 'Jackets', 'Tops', 'Trend']
    possible_classes = ['Blouses', 'Dresses', 'Fine gauge', 'Intimates', 'Jackets', 'Jeans', 'Knits', 'Layering', 'Legwear', 'Lounge', 'Outerwear', 'Pants', 'Shorts', 'Skirts', 'Sleep', 'Sweaters', 'Swim', 'Trend']
    
    for division in possible_divisions:
        features_dict[f'Division Name_{division}'] = [1 if division == division_name else 0]
    
    for department in possible_departments:
        features_dict[f'Department Name_{department}'] = [1 if department == department_name else 0]
    
    for class_ in possible_classes:
        features_dict[f'Class Name_{class_}'] = [1 if class_ == class_name else 0]

    # Ensure all possible feature columns are present, set to 0 if not in this instance
    all_possible_features = [
        'Rating', 'Positive Feedback Count', 'Cluster', 'Age_Group',
        'Division Name_General', 'Division Name_General Petite', 'Division Name_Initmates',
        'Department Name_Bottoms', 'Department Name_Dresses', 'Department Name_Intimate',
        'Department Name_Jackets', 'Department Name_Tops', 'Department Name_Trend',
        'Class Name_Blouses', 'Class Name_Dresses', 'Class Name_Fine gauge', 'Class Name_Intimates',
        'Class Name_Jackets', 'Class Name_Jeans', 'Class Name_Knits', 'Class Name_Layering',
        'Class Name_Legwear', 'Class Name_Lounge', 'Class Name_Outerwear', 'Class Name_Pants',
        'Class Name_Shorts', 'Class Name_Skirts', 'Class Name_Sleep', 'Class Name_Sweaters',
        'Class Name_Swim', 'Class Name_Trend', 'nb_pred', 'log_pred', 'svc_pred', 'rf_pred'
    ]
    
    for feature in all_possible_features:
        if feature not in features_dict:
            features_dict[feature] = [0]
    
    # Create a DataFrame for the features
    features_df = pd.DataFrame(features_dict)
    
    # Reorder columns to ensure they match the specified order
    features_df = features_df[all_possible_features]
    
    # Print the feature DataFrame for debugging
    print(f"Features DataFrame: {features_df}")
    

    # Predict with the XGBoost model
    try:
        prediction = model.predict(features_df)
    except ValueError as e:
        print(f"Error during prediction: {e}")
        raise
    # Print the raw prediction for debugging
    print(prediction[0] == 1)

    return prediction[0] == 1