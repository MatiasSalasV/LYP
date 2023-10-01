from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # #URL que redirige a la página de inicio de sesión
    #path('accounts/login/', login_view, name="login"),
    #path("logout/", LogoutView.as_view(), name="logout"),
    
    #URL que redirige a la página del administrador
    #path("home/admin/", home_admin, name="home_admin"),

    #URL que redirige a la página de acerca de nosotros
    path("", views.index.as_view(), name="index"),

    #URL que redirige a la página de acerca de nosotros
    path("nosotros/", views.nosotros.as_view(), name="nosotros"),

    #URL que redirige a la página de proyectos
    path("proyectos/", views.proyectos.as_view(), name="proyectos"),

    #URL que redirige a la página de contácto
    path("contacto/", views.contacto.as_view(), name="contacto"),

    #URL para registrar usuario
    path("registro/", views.registro_usuario, name='registro_usuario'),

    path('login/', views.login, name='login'),

    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),

    #URL para la vista de perfil
    path('perfil/', views.ver_perfil, name='ver_perfil'),  



]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

