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
    email = models.EmailField(("Correo"),unique=True)
    nombre = models.CharField(("Nombre"),max_length=100,null=True,blank=True)
    apellido = models.CharField(("Apellido"),max_length=100,null=True,blank=True)
    tipo_usuario = models.CharField(("Tipo usuario"),max_length=20,choices=TIPO_USUARIO_CHOICES,null=True,blank=True,default='')
    nombre_empresa = models.CharField(("Nombre empresa"), max_length=50,null=True,blank=True)
    foto_perfil = models.ImageField("Foto de perfil", upload_to='fotos_perfil/', blank=True, null=True)    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    fecha_registro = models.DateField(("Fecha de Registro"), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'tipo_usuario']

    def ver_perfil(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario,
            'nombre_empresa': self.nombre_empresa,
            'foto_perfil': self.foto_perfil,
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
        return f"{self.nombre_proyecto} - {self.usuario.nombre + ' ' + self.usuario.apellido}"
    
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
    archivo_certificacion = models.FileField(upload_to='certificaciones/', null=True, blank=True)

    def actualizar_certificacion(self, nuevo_nombre=None, nueva_fecha=None, nuevo_archivo=None):
        if nuevo_nombre:
            self.nombre_certificacion = nuevo_nombre
        if nueva_fecha:
            self.fecha_obtencion = nueva_fecha
        if nuevo_archivo:
            self.archivo_certificacion = nuevo_archivo
        self.save()

    def ver_certificacion(self):
        return {
            'nombre_certificacion': self.nombre_certificacion,
            'fecha_obtencion': self.fecha_obtencion,
            'archivo_certificacion': self.archivo_certificacion.url if self.archivo_certificacion else None,
        }
    
    def anos_desde_obtencion(self):
        return (date.today() - self.fecha_obtencion).days // 365

    def meses_desde_obtencion(self):
        return (date.today() - self.fecha_obtencion).days // 30

    def __str__(self):
        return f"{self.nombre_certificacion} - {self.usuario.nombre + ' ' + self.usuario.apellido}"
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

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
    foto_proyecto = models.ImageField("Foto proyecto", upload_to='fotos_proyecto/', blank=True, null=True) 
    categorias = models.ManyToManyField(Categoria, related_name='proyectos')  
    fecha_publicacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='publicado')

    def iniciar_proyecto(self):
        self.estado = 'en_ejecucion'
        self.save()

    def ver_proyecto(self):
        return {
            'usuario': self.usuario.nombre + ' ' + self.usuario.apellido,  # Asumiendo que quieres mostrar el email del usuario. Puedes cambiarlo por otro campo si lo prefieres.
            'nombre_proyecto': self.nombre_proyecto,
            'descripcion': self.descripcion,
            'foto_proyecto': self.foto_proyecto.url if self.foto_proyecto else None,  # Devuelve la URL de la imagen si existe, de lo contrario None.
            'fecha_publicacion': self.fecha_publicacion,
            'estado': self.get_estado_display(),  # Utiliza get_estado_display() para obtener la representación legible del estado.
        }
    
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
    
    def save(self, *args, **kwargs):
        if self.usuario.tipo_usuario != 'Constructora':
            raise ValueError("Solo un usuario de tipo 'Constructora' puede publicar un proyecto.")
        super(Proyecto, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre_proyecto} - {self.usuario.nombre + ' ' + self.usuario.apellido}. Publicado el: {self.fecha_publicacion}"

class Presupuesto(models.Model):
    ESTADOS = (
        ('borrador', 'Borrador'),
        ('enviado', 'Enviado'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    )

    proyecto = models.ForeignKey('Proyecto', related_name='presupuestos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(get_user_model(), related_name='presupuestos', on_delete=models.CASCADE)
    descripcion = models.TextField(("Descripción de presupuesto"))
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    documento_adjunto = models.FileField("Documento adjunto", upload_to='documentos_presupuesto/', blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_envio = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='borrador')

    def cambiar_estado(self, nuevo_estado):
        if self.estado in ['Aceptado', 'Rechazado'] and nuevo_estado != self.estado:
            raise ValueError(f"El presupuesto ya ha sido {self.estado}. No se puede cambiar a {nuevo_estado}.")

        if nuevo_estado == 'Aceptado':
            presupuesto_aceptado_existente = Presupuesto.objects.filter(proyecto=self.proyecto, estado='Aceptado').exclude(id=self.id).exists()
            if presupuesto_aceptado_existente:
                raise ValueError("Ya existe un presupuesto aceptado para este proyecto.")
            
        if nuevo_estado in dict(self.ESTADOS).keys():
            self.estado = nuevo_estado
            if self.estado == 'Aceptado':
                self.proyecto.iniciar_proyecto()
            self.save()

    def ver_presupuesto(self):
        return {
            'proyecto': self.proyecto.nombre_proyecto,
            'usuario': (self.usuario.nombre or "") + " " + (self.usuario.apellido or ""),
            'descripcion': self.descripcion,
            'monto': self.monto,
            'documento_adjunto': self.documento_adjunto.url if self.documento_adjunto else None,
            'fecha_creacion': self.fecha_creacion,
            'fecha_envio': self.fecha_envio,
            'estado': self.get_estado_display(),
        }
    
    def enviar(self):
        self.estado = 'enviado'
        self.fecha_envio = date.today()
        self.save()

    def es_aceptado(self):
        return self.estado == 'Aceptado'
    
    def es_rechazado(self):
        return self.estado == 'Rechazado'
    
    def actualizar_presupuesto(self, nueva_descripcion=None, nuevo_monto=None, nuevo_documento=None):
        if nueva_descripcion:
            self.descripcion = nueva_descripcion
        if nuevo_monto:
            self.monto = nuevo_monto
        if nuevo_documento:
            self.documento_adjunto = nuevo_documento
        self.save()

    def __str__(self):
        return f"Presupuesto para {self.proyecto.nombre_proyecto} - Ejecutado por: {self.usuario.nombre + ' ' +self.usuario.apellido} - Enviado el: {self.fecha_envio}"


    