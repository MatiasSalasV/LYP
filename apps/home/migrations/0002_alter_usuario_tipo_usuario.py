# Generated by Django 4.2.3 on 2023-09-28 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(blank=True, choices=[('Contratista', 'Contratista'), ('Constructora', 'Constructora')], max_length=20, null=True, verbose_name='Tipo usuario'),
        ),
    ]
