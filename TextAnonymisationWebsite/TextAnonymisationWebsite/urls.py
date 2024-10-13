"""
URL configuration for TextAnonymisationWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from anon_website.views import finished_registration_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/', admin.site.urls),
    # path('api/v1/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls')),
    path('website/', include("anon_website.urls")), 
    path('finished_registration/', finished_registration_view, name='finished_registration'),
    path('website-auth/', include("web_auth.urls")), # Auth routes - login / register
]
