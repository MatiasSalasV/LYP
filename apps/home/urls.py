from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
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

    # #URL para ver todas las experiencias
    path('experiencias/', views.ver_todas_experiencias, name='ver_todas_experiencias'),

    #URL para editar experiencia
    path('experiencias/<int:pk>/editar', views.editar_experiencia, name='editar_experiencia'),

    #URL para eliminar experiencia
    path('experiencias/<int:pk>/eliminar/', views.eliminar_experiencia, name='eliminar_experiencia'),

    # #URL para ver todas las certificiones
    path('certificaciones/', views.ver_todas_certificaciones, name='ver_todas_certificaciones'),

    #URL para editar certificacion
    path('certificaciones/<int:pk>/editar', views.editar_certificacion, name='editar_certificacion'),

    #URL para eliminar certificacion
    path('certificaciones/<int:pk>/eliminar/', views.eliminar_certificacion, name='eliminar_certificacion'),

    #URL para crear proyecto
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),

    #URL para editar proyecto
    path('proyectos/<int:pk>/editar/', views.editar_proyecto, name='editar_proyecto'),

    #URL para eliminar proyecto
    path('proyectos/<int:pk>/eliminar/', views.eliminar_proyecto, name='eliminar_proyecto'),

    #URL para ver solo poryectos del usuario que los publica
    path('mis_proyectos/', views.ver_mis_proyectos, name='ver_mis_proyectos'),


    #URL para ver todos los proyectos
    path('proyectos1/', views.ver_todos_proyectos, name='ver_todos_proyectos'),

    #URL para ver un proyecto específico
    path('proyectos/<int:pk>/', views.ver_proyecto, name='ver_proyecto'),


]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

