# Generated by Django 4.2.3 on 2023-10-08 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre')),
                ('apellido', models.CharField(blank=True, max_length=100, null=True, verbose_name='Apellido')),
                ('tipo_usuario', models.CharField(blank=True, choices=[('', '--- Selecciona el tipo de usuario ---'), ('Contratista', 'Contratista'), ('Constructora', 'Constructora')], default='', max_length=20, null=True, verbose_name='Tipo usuario')),
                ('nombre_empresa', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre empresa')),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='fotos_perfil/', verbose_name='Foto de perfil')),
                ('presentacion', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='Fecha de Registro')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proyecto', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('foto_proyecto', models.ImageField(blank=True, null=True, upload_to='fotos_proyecto/', verbose_name='Foto proyecto')),
                ('fecha_publicacion', models.DateField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('publicado', 'Publicado'), ('en_ejecucion', 'En Ejecución'), ('completado', 'Completado'), ('cancelado', 'Cancelado')], default='publicado', max_length=50)),
                ('categorias', models.ManyToManyField(related_name='proyectos', to='home.categoria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyectos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(verbose_name='Descripción de presupuesto')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=12)),
                ('documento_adjunto', models.FileField(blank=True, null=True, upload_to='documentos_presupuesto/', verbose_name='Documento adjunto')),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('fecha_envio', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('borrador', 'Borrador'), ('enviado', 'Enviado'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')], default='borrador', max_length=50)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presupuestos', to='home.proyecto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presupuestos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experiencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proyecto', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('descripcion_proyecto', models.TextField(blank=True, null=True)),
                ('funciones', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiencias', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Experiencia',
                'verbose_name_plural': 'Experiencias',
            },
        ),
        migrations.CreateModel(
            name='Certificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_certificacion', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_obtencion', models.DateField()),
                ('archivo_certificacion', models.FileField(blank=True, null=True, upload_to='certificaciones/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificaciones', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
