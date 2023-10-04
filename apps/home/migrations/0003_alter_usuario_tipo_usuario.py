# Generated by Django 4.2.3 on 2023-09-28 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(blank=True, choices=[('', '--- Selecciona el tipo de usuario ---'), ('Contratista', 'Contratista'), ('Constructora', 'Constructora')], default='', max_length=20, null=True, verbose_name='Tipo usuario'),
        ),
    ]