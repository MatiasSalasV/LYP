"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views import defaults

# handler404 = 'apps.home.views.error_404'
handler404 = 'apps.home.views.error_404_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.authentication.urls")),
    path("", include("apps.home.urls")),    
    path("", include("apps.contratista.urls")),
    path("", include("apps.holding.urls")),    

    
    
    #URL PRINCIPAL QUE MUESTRA EL HOME DE LA PÁGINA AL INGRESAR Al Localhost http://127.0.0.1:8000/ 
    path('', TemplateView.as_view(template_name='index.html'), name='index'),


]

