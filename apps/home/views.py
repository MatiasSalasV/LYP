from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm, LoginForm, UsuarioForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


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
            messages.success(request, f'Cuenta creada para {username}!')
            return redirect('index')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'forms/registro_usuario.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'forms/login.html', {'form': form})

@login_required  # Esto asegura que solo usuarios logueados pueden acceder a esta vista
def ver_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado con éxito!')
            return redirect('ver_perfil')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuario/ver_perfil.html', {'perfil': usuario, 'form': form})

