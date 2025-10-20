from django.shortcuts import render, redirect
from .forms import FormTipoSolicitud
from .models import TipoSolicitud


def bienvenida(request):
    return render(request, 'bienvenida.html')


def lista_solicitudes(request):
    context = {
        'tipo_solicitudes': TipoSolicitud.objects.all()
    }
    return render(request, 'lista_tipo_solicitudes.html', context)

def agregar(request):
    if request.method == 'POST':
        form = FormTipoSolicitud(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tipo_solicitudes')
    else:
        form = FormTipoSolicitud()
    context = {
        'form': form
    }
    return render(request, 'agregar_solicitud.html', context)
