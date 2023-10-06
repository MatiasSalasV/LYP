from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Experiencia, Certificacion
from django.contrib.auth import get_user_model


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
        fields = ['nombre', 'apellido', 'email', 'tipo_usuario', 'nombre_empresa', 'foto_perfil']
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
    class Meta:
        model = Experiencia
        fields = ['nombre_proyecto', 'fecha_inicio', 'fecha_fin', 'descripcion_proyecto', 'funciones']

class CertificacionForm(forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = ['nombre_certificacion', 'fecha_obtencion', 'archivo_certificacion']