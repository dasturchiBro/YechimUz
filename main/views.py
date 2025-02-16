from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Food
from math import radians, cos, sin, asin, sqrt
from django.http import JsonResponse
from django.contrib import messages
CustomUser = get_user_model()

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")

            # ✅ Check if username already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already taken! Choose a different one.")
                return render(request, "registration/signup.html", {"form": form})

            # ✅ Create user if username is unique
            user = form.save()
            login(request, user)
            return redirect("/dashboard/")

    else:
        form = CustomUserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard")  # Redirect to dashboard
            else:
                messages.error(request, "Invalid username or password")  # Show error message
        else:
            messages.error(request, "Invalid form submission. Please check your input.")  # Show form errors

    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})

@login_required
def dashboard_view(request):
    if hasattr(request.user, 'user_type'):
        user_type = request.user.user_type
    else:
        user_type = 'customer'  # Default to customer if not set

    return render(request, 'dashboard.html', {'user_type': user_type})
    
def logout_view(request):
    logout(request)
    return redirect("/")


    # CUSTOMS
def home(request):
	return render(request, 'index.html', {})

def blog(request):
    return render(request, 'blog.html', {})

def contact(request):
    return render(request, 'contact.html', {})


def about(request):
	return render(request, 'about.html', {})

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
##########____________________FOOOOOOOD______________############
    # Haversine formula to calculate distance between two points (lat/lon)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in KM
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c  # Distance in KM

# API to get nearby food
def get_nearby_food(request):
    user_lat = float(request.GET.get('lat'))
    user_lon = float(request.GET.get('lon'))
    max_distance = 5  # Show food within 5 KM radius

    nearby_food = []
    for food in Food.objects.all():
        distance = haversine(user_lat, user_lon, food.latitude, food.longitude)
        if distance <= max_distance:
            nearby_food.append({
                'name': food.name,
                'description': food.description,
                'price': float(food.price),
                'discount_price': float(food.discount_price) if food.discount_price else None,
                'latitude': food.latitude,
                'longitude': food.longitude
            })

    return JsonResponse({'food': nearby_food})