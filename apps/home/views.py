from django.shortcuts import render
from django.views.generic import TemplateView

class index(TemplateView):
    template_name = 'index.html'

class nosotros(TemplateView):
    template_name = 'nosotros.html'

class proyectos(TemplateView):
    template_name = 'proyectos.html'

class contacto(TemplateView):
    template_name = 'contacto.html'


