from django.views.generic import TemplateView
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView,DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden


class index(TemplateView):
    template_name = 'index.html'

class nosotros(TemplateView):
    template_name = 'nosotros.html'

class proyectos(TemplateView):
    template_name = 'proyectos.html'

class contacto(TemplateView):
    template_name = 'contacto.html'




def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')  # Obtiene la contraseña ingresada en el formulario
            user = authenticate(request, username=username, password=password)  # Autentica al usuario
            if user is not None:
                auth_login(request, user)  # Inicia la sesión del usuario
            messages.success(request, f'Cuenta creada para {username}')
            return redirect('ver_perfil')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'forms/registro_usuario.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # messages.success(request, '¡Inicio de sesión exitoso!')
            return redirect('ver_perfil')
        else:
            messages.error(request, 'Correo y/o contraseña inválidos. Por favor, inténtelo de nuevo.')
            form = LoginForm()
    else:
        form = LoginForm()
    return render(request, 'forms/login.html', {'form': form})

@login_required  # Esto asegura que solo usuarios logueados pueden acceder a esta vista
def ver_perfil(request):
    usuario = request.user
    experiencias = usuario.experiencias.all()
    certificaciones = usuario.certificaciones.all()
    proyectos = usuario.proyectos.all()
    form_experiencia = ExperienciaForm()
    form_certificacion = CertificacionForm()
    # form_foto_perfil = request.user

    if request.method == 'POST':
        submit_button = request.POST.get('submit_button')

        if submit_button == 'usuario':
            form = UsuarioForm(request.POST, request.FILES, instance=usuario)
            if form.is_valid():
                form.save()
                messages.success(request, 'Perfil actualizado con éxito')
                return redirect('ver_perfil')
            
        elif submit_button == 'experiencia':
            form_experiencia = ExperienciaForm(request.POST)
            if form_experiencia.is_valid():
                experiencia = form_experiencia.save(commit=False)
                experiencia.usuario = request.user
                experiencia.save()
                messages.success(request, 'Experiencia agregada con éxito')
                return redirect('ver_perfil')
            
        elif submit_button == 'certificacion':
            form_certificacion = CertificacionForm(request.POST, request.FILES)
            if form_certificacion.is_valid():
                certificacion = form_certificacion.save(commit=False)
                certificacion.usuario = request.user
                certificacion.save()
                messages.success(request, 'Certificación agregada con éxito')
                return redirect('ver_perfil')
        
        elif submit_button == 'fotoperfil':
            form_foto_perfil = FotoPerfil(request.POST, request.FILES, instance=usuario)
            if form_foto_perfil.is_valid():
                form_foto_perfil.save()
                messages.success(request, 'Foto de perfil actualizada con éxito')
                return redirect('ver_perfil')

    else:
        form = UsuarioForm(instance=usuario)
        form_foto_perfil = FotoPerfil(instance=usuario)

    contexto = {
        'perfil':usuario,
        'form': form,
        'form_experiencia': form_experiencia,
        'form_certificacion': form_certificacion,
        'form_foto_perfil': form_foto_perfil,
        'experiencias': experiencias,
        'certificaciones': certificaciones,
        'proyectos':proyectos,
    }

    return render(request, 'usuario/ver_perfil.html', contexto)

@login_required
def ver_todas_experiencias(request):
    usuario = request.user
    todas_experiencias = usuario.experiencias.all()

    contexto = {
        'experiencias': todas_experiencias,
    }
    return render(request, 'usuario/todas_experiencias.html', contexto)

@login_required
def editar_experiencia(request, pk):
    experiencia = get_object_or_404(Experiencia, pk=pk)
    if experiencia.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para editar esta experiencia.")
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiencia actualizada con éxito')
            return redirect(reverse('ver_todas_experiencias'))
    else:
        form = ExperienciaForm(instance=experiencia)
    contexto = {
        'form': form,
    }
    return render(request, 'usuario/editar_experiencia.html', contexto)

@login_required
def eliminar_experiencia(request, pk):
    experiencia = get_object_or_404(Experiencia,pk=pk)
    if experiencia.usuario == request.user:
        if request.method == 'POST':
            experiencia.delete()
            messages.success(request, 'Experiencia eliminada con éxito.')
            return redirect('ver_todas_experiencias')
        return render(request, 'usuario/eliminar_experiencia.html', {'experiencia': experiencia})
    
    else:
        # El usuario no es el propietario, muestra un mensaje de error
        messages.error(request, 'No tienes permiso para eliminar esta experiencia.')
        return redirect('ver_todas_experiencias')


@login_required
def ver_todas_certificaciones(request):
    usuario = request.user
    todas_certificaciones = usuario.certificaciones.all()

    contexto = {
        'certificaciones': todas_certificaciones,
    }
    return render(request, 'usuario/todas_certificaciones.html', contexto)

@login_required
def editar_certificacion(request, pk):
    certificacion = get_object_or_404(Certificacion, pk=pk)
    if certificacion.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para editar esta certificación.")
    if request.method == 'POST':
        form = CertificacionForm(request.POST, instance=certificacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certificación actualizada con éxito')            
            return redirect(reverse('ver_todas_certificaciones'))
    else:
        form = CertificacionForm(instance=certificacion)
    contexto = {
        'form': form,
    }
    return render(request, 'usuario/editar_certificacion.html', contexto)


@login_required
def eliminar_certificacion(request, pk):
    certificacion = get_object_or_404(Certificacion,pk=pk)
    if certificacion.usuario == request.user:
        if request.method == 'POST':
            certificacion.delete()
            messages.success(request,'Certificación eliminada con éxito.')
            return redirect('ver_todas_certificaciones')
        return render(request, 'usuario/eliminar_certificacion.html',{'certificacion':certificacion})
    
    else:
        # El usuario no es el propietario, muestra un mensaje de error
        messages.error(request, 'No tienes permiso para eliminar esta certificación.')
        return redirect('ver_todas_certificaciones')
    


def error_404_view(request, exception):
    return render(request, 'errors/error404.html', status=404)

@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.usuario = request.user  # Asigna el usuario actual como propietario del proyecto
            if proyecto.usuario.tipo_usuario != 'Constructora':
                messages.error(request, 'Solo un usuario de tipo Constructora puede publicar un proyecto.')
            
            else:
                proyecto.save()
                messages.success(request, 'Proyecto creado con éxito')
                return redirect('ver_mis_proyectos')  # Redirige a la vista de detalles del proyecto
            
    else:
        form = ProyectoForm()
    
    return render(request, 'projects/crear_proyecto.html', {'form': form})

@login_required
def editar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)

    # Verifica que el usuario que intenta editar sea el mismo que creó el proyecto
    if proyecto.usuario != request.user:
        messages.error(request, 'No tienes permiso para editar este proyecto.')
        return redirect('ver_mis_proyectos')

    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            proyecto = form.save()
            messages.success(request, 'Proyecto actualizado con éxito')
            return redirect('ver_mis_proyectos')
    else:
        form = ProyectoForm(instance=proyecto)

    return render(request, 'projects/editar_proyecto.html', {'form': form, 'proyecto': proyecto})


@login_required
def eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)

    # Verifica que el usuario que intenta eliminar sea el mismo que creó el proyecto
    if proyecto.usuario != request.user:
        messages.error(request, 'No tienes permiso para eliminar este proyecto.')
        return redirect('ver_mis_proyectos')

    if request.method == 'POST':
        # El usuario ha confirmado la eliminación, elimina el proyecto
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado con éxito')
        return redirect('ver_mis_proyectos')

    return render(request, 'projects/eliminar_proyecto.html', {'proyecto': proyecto})

@login_required
def ver_mis_proyectos(request):
    proyectos = Proyecto.objects.filter(usuario=request.user)
    return render(request, 'projects/ver_mis_proyectos.html', {'proyectos': proyectos})

@login_required
def ver_todos_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'projects/ver_todos_proyectos.html', {'proyectos': proyectos})

@login_required
def ver_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    categorias_proyecto = proyecto.categorias.all()  # Obtiene todas las categorías asociadas al proyecto
    print(f'ESTAS SON AS CATEGIRIAS: {categorias_proyecto}')
    return render(request, 'projects/ver_proyecto.html', {
        'proyecto': proyecto,
        'categorias': categorias_proyecto,
    })