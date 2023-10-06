from django.contrib import admin
from .models import Usuario, Experiencia, Certificacion, Proyecto, Presupuesto, Categoria

# Registra tus modelos aquí

admin.site.register(Usuario)
admin.site.register(Experiencia)
admin.site.register(Certificacion)
admin.site.register(Proyecto)
admin.site.register(Presupuesto)
admin.site.register(Categoria)
