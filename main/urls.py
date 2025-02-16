from django.urls import path
from django.conf.urls import handler404
from .views import signup_view, login_view, dashboard_view, logout_view, home, about, custom_404_view, get_nearby_food, blog, contact
handler404 = custom_404_view
urlpatterns = [
    path('', home, name="home"),
    path('about', about, name="about"),
    path('contact', contact, name="contact"),
    path('blog', blog, name="blog"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path('api/nearby_food/', get_nearby_food, name='nearby_food'),
]
