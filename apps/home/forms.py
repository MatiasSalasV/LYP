from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Experiencia, Certificacion, Proyecto, Categoria
from django.contrib.auth import get_user_model
from django.urls import reverse


class RegistroUsuarioForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="",  # Aquí se ajusta el help_text para el campo de la contraseña
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="",  # Aquí se ajusta el help_text para el campo de confirmación de contraseña
    )
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellido', 'foto_perfil', 'tipo_usuario', 'nombre_empresa', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),  
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_tipo_usuario(self):
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        if tipo_usuario == '':
            raise forms.ValidationError('Debes seleccionar un tipo de usuario.')
        return tipo_usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'tipo_usuario', 'nombre_empresa','presentacion']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'presentacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FotoPerfil(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto_perfil']
        widgets = {
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),  
        }

    
class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Correo', 
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ExperienciaForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',),
        required=False
    )
    class Meta:
        model = Experiencia
        fields = ['nombre_proyecto', 'fecha_inicio', 'fecha_fin', 'descripcion_proyecto', 'funciones']
        widgets = {
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proyecto'}),
            # 'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # 'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion_proyecto': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descripción general del proyecto'}),
            'funciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detalles de tus responsabilidades y funciones en el proyecto'}),
        }

class CertificacionForm(forms.ModelForm):
    fecha_obtencion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        input_formats=('%Y-%m-%d',)
    )
    class Meta:
        model = Certificacion
        fields = ['nombre_certificacion', 'fecha_obtencion', 'archivo_certificacion']
        widgets = {
            'nombre_certificacion': forms.TextInput(attrs={'class': 'form-control'}),
            # 'fecha_obtencion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'archivo_certificacion': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre_proyecto', 'descripcion', 'foto_proyecto', 'categorias', 'estado']
        widgets = {
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'foto_proyecto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categorias': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
