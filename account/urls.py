from django.urls import path
from .views import signup_view, UserLoginView, logout_view


app_name = "account"
urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
