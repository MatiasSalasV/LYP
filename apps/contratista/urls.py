from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # #URL que redirige a la página de inicio de sesión
    #path('accounts/login/', login_view, name="login"),
    #path("logout/", LogoutView.as_view(), name="logout"),
    
    #URL que redirige a la página del administrador
    #path("home/admin/", home_admin, name="home_admin"),

    #URL que redirige a la página del funcionario
    #path("home/funcionario/", home_funcionario, name="home_funcionario"),



]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

