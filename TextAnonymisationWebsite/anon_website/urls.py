from django.urls import path, include
from anon_website.views import anonymise_view, home_view, login_view, try_view, signup_view, finished_registration_view

app_name = "anon_website"

urlpatterns = [
    path('', anonymise_view, name='anonymise'),
    path('try/', try_view, name='try'),
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
]
