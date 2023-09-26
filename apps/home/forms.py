from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput,
        help_text="",  # Aquí se ajusta el help_text para el campo de la contraseña
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        strip=False,
        help_text="",  # Aquí se ajusta el help_text para el campo de confirmación de contraseña
    )
    class Meta:
        model = Usuario
        fields = ['email', 'nombre_completo', 'tipo_usuario', 'nombre_empresa', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))