from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from datetime import date


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo email debe estar definido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO_CHOICES = [
        ('', '--- Selecciona el tipo de usuario ---'),
        ('Contratista', 'Contratista'),
        ('Constructora', 'Constructora')
    ]
    email = models.EmailField(("Email"),unique=True)
    nombre_completo = models.CharField(("Nombre"),max_length=100,null=True,blank=True)
    tipo_usuario = models.CharField(("Tipo usuario"),max_length=20,choices=TIPO_USUARIO_CHOICES,null=True,blank=True,default='')
    nombre_empresa = models.CharField("Nombre empresa", max_length=50,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre_completo', 'tipo_usuario', 'nombre_empresa']

    def ver_perfil(self):
        return {
            'nombre_completo': self.nombre_completo,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario,
            'nombre_empresa': self.nombre_empresa,
        }
    
    def publicar_proyecto(self, nombre_proyecto, descripcion):
        if self.es_constructora():
            Proyecto.objects.create(
                usuario=self,
                nombre_proyecto=nombre_proyecto,
                descripcion=descripcion
            )

    def enviar_presupuesto(self, proyecto_id, descripcion, monto):
        if self.es_contratista():
            proyecto = Proyecto.objects.get(id=proyecto_id)
            Presupuesto.objects.create(
                proyecto=proyecto,
                usuario=self,
                descripcion=descripcion,
                monto=monto
            )

    def ver_proyectos_disponibles(self):
        if self.es_contratista():
            return Proyecto.objects.filter(estado='publicado')
        
    def ver_presupuestos_enviados(self):
        if self.es_contratista():
            return Presupuesto.objects.filter(usuario=self)

    def ver_presupuestos_recibidos(self):
        if self.es_constructora():
            return Presupuesto.objects.filter(proyecto__usuario=self)

    def activar_usuario(self):
        self.is_active = True
        self.save()

    def desactivar_usuario(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.email
    
    def es_contratista(self):
        return self.tipo_usuario == 'Contratista'
    
    def es_constructora(self):
        return self.tipo_usuario == 'Constructora'

class Experiencia(models.Model):
    usuario = models.ForeignKey(get_user_model(), related_name='experiencias', on_delete=models.CASCADE)
    nombre_proyecto = models.CharField(max_length=255,null=True,blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion_proyecto = models.TextField(help_text="Descripción general del proyecto.")
    funciones = models.TextField(help_text="Detalles de tus responsabilidades y funciones en el proyecto.")

    def __str__(self):
        return f"{self.nombre_proyecto} - {self.usuario.nombre_completo}"
    
    class Meta:
        verbose_name = "Experiencia"
        verbose_name_plural = "Experiencias"

    def duracion_proyecto(self):
        if self.fecha_fin:
            return (self.fecha_fin - self.fecha_inicio).days
        else:
            return (date.today() - self.fecha_inicio).days
        
    def actualizar_experiencia(self, nueva_fecha_inicio=None, nueva_fecha_fin=None, nueva_descripcion=None, nuevas_funciones=None):
        if nueva_fecha_inicio:
            self.fecha_inicio = nueva_fecha_inicio
        if nueva_fecha_fin:
            self.fecha_fin = nueva_fecha_fin
        if nueva_descripcion:
            self.descripcion_proyecto = nueva_descripcion
        if nuevas_funciones:
            self.funciones = nuevas_funciones
        self.save()

    def ver_experiencia(self):
        return {
            'nombre_proyecto': self.nombre_proyecto,
            'descripcion_proyecto': self.descripcion_proyecto,
            'funciones': self.funciones,
            'duracion': self.duracion_proyecto(),
        }

class Certificacion(models.Model):
    usuario = models.ForeignKey(get_user_model(), related_name='certificaciones', on_delete=models.CASCADE)
    nombre_certificacion = models.CharField(max_length=255, null=True,blank=True)
    fecha_obtencion = models.DateField()

    def actualizar_certificacion(self, nuevo_nombre=None, nueva_fecha=None):
        if nuevo_nombre:
            self.nombre_certificacion = nuevo_nombre
        if nueva_fecha:
            self.fecha_obtencion = nueva_fecha
        self.save()

    def ver_certificacion(self):
        return {
            'nombre_certificacion': self.nombre_certificacion,
            'fecha_obtencion': self.fecha_obtencion,
        }
    
    def anos_desde_obtencion(self):
        return (date.today() - self.fecha_obtencion).days // 365

    def meses_desde_obtencion(self):
        return (date.today() - self.fecha_obtencion).days // 30

    def __str__(self):
        return f"{self.nombre_certificacion} - {self.usuario.nombre_completo}"

class Proyecto(models.Model):
    ESTADOS = (
        ('publicado', 'Publicado'),
        ('en_ejecucion', 'En Ejecución'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )

    usuario = models.ForeignKey(get_user_model(), related_name='proyectos', on_delete=models.CASCADE)
    nombre_proyecto = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='publicado')

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS).keys():
            self.estado = nuevo_estado
            self.save()
            return True
        return False

    def ver_proyecto(self):
        return {
            'nombre_proyecto': self.nombre_proyecto,
            'descripcion': self.descripcion,
            'fecha_publicacion': self.fecha_publicacion,
            'estado': self.estado,
        }

    def es_publicado(self):
        return self.estado == 'publicado'
    
    def es_completado(self):
        return self.estado == 'completado'
    
    def actualizar_proyecto(self, nuevo_nombre=None, nueva_descripcion=None, nuevo_estado=None):
        if nuevo_nombre:
            self.nombre_proyecto = nuevo_nombre
        if nueva_descripcion:
            self.descripcion = nueva_descripcion
        if nuevo_estado:
            self.estado = nuevo_estado
        self.save()
    
    def dias_desde_publicacion(self):
        return (date.today() - self.fecha_publicacion).days
    
    def __str__(self):
        return f"{self.nombre_proyecto} - {self.usuario.nombre_completo}. Publicado el: {self.fecha_publicacion}"

class Presupuesto(models.Model):
    ESTADOS = (
        ('enviado', 'Enviado'),
        ('en_revision', 'En Revisión'),
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
    )

    proyecto = models.ForeignKey('Proyecto', related_name='presupuestos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(get_user_model(), related_name='presupuestos', on_delete=models.CASCADE)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_envio = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='enviado')

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS).keys():
            self.estado = nuevo_estado
            self.save()

    def ver_presupuesto(self):
        return {
            'proyecto': self.proyecto.nombre_proyecto,
            'usuario': self.usuario.nombre_completo,
            'descripcion': self.descripcion,
            'monto': self.monto,
            'fecha_envio': self.fecha_envio,
            'estado': self.get_estado_display(),
        }

    def es_aceptado(self):
        return self.estado == 'Aceptado'
    
    def es_rechazado(self):
        return self.estado == 'Rechazado'
    
    def actualizar_presupuesto(self, nueva_descripcion=None, nuevo_monto=None):
        if nueva_descripcion:
            self.descripcion = nueva_descripcion
        if nuevo_monto:
            self.monto = nuevo_monto
        self.save()

    def __str__(self):
        return f"Presupuesto para {self.proyecto.nombre_proyecto} - Ejecutado por: {self.usuario.nombre_completo} - Enviado el: {self.fecha_envio}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class ProyectoCategoria(models.Model):
    proyecto = models.ForeignKey('Proyecto', related_name='categorias', on_delete=models.CASCADE)
    categoria = models.ForeignKey('Categoria', related_name='proyectos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.proyecto.nombre_proyecto} - {self.categoria.nombre}"
    
    def eliminar_asociacion(self):
        self.delete()

    def es_categoria_de_proyecto(self, proyecto_id):
        return self.proyecto.id == proyecto_id