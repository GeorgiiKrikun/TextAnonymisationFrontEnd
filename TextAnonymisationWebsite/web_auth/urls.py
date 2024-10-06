from django.urls import path, include
from .views import login_view, signup_view, logout_view, reset_password_view, activate, reset_password_link_view
from django.contrib.auth.views import LogoutView

app_name = "web_auth"

urlpatterns = [
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', logout_view, name="logout"),
    path("reset_password/", reset_password_view, name="reset_password"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path('reset_password_link/<uidb64>/<token>/', reset_password_link_view, name='reset_password_link'),
    # path('social_login/', include('allauth.urls'),),
]
