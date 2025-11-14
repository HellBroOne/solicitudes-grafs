from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormTipoSolicitud
from .models import TipoSolicitud
from .funcionalidad import FuncionesAvanzadas
from .models import TipoSolicitud, FormularioSolicitud, CampoFormulario, Solicitud, RespuestaCampo, ArchivoAdjunto
from .models import SeguimientoSolicitud
import uuid



def bienvenida(request):
    return render(request, 'bienvenida.html')


def lista_solicitudes(request):
    funciones_avanzadas = FuncionesAvanzadas()
    resultado = funciones_avanzadas.calculo_extremo(2, 2)
    context = {
        'tipo_solicitudes': TipoSolicitud.objects.all(),
        'resultado': resultado
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


def crear_solicitud(request, tipo_id):
    tipo = get_object_or_404(TipoSolicitud, id=tipo_id)
    formulario = tipo.formulario
    campos = formulario.campos.all()

    if request.method == 'POST':
        # Crear folio único
        folio = str(uuid.uuid4())[:8]

        solicitud = Solicitud.objects.create(
            usuario=request.user,
            tipo_solicitud=tipo,
            folio=folio
        )

        # Guardar respuestas
        for campo in campos:
            valor = request.POST.get(campo.nombre, '')

            respuesta = RespuestaCampo.objects.create(
                solicitud=solicitud,
                campo=campo,
                valor=valor
            )

            # Si es archivo
            if campo.tipo == 'file':
                archivos = request.FILES.getlist(campo.nombre)
                for archivo in archivos:
                    ArchivoAdjunto.objects.create(
                        solicitud=solicitud,
                        respuesta=respuesta,
                        archivo=archivo,
                        nombre=archivo.name
                    )

        return redirect('mis_solicitudes')

    context = {
        'tipo': tipo,
        'formulario': formulario,
        'campos': campos
    }
    return render(request, 'alumno/crear_solicitud.html', context)

def mis_solicitudes(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'alumno/mis_solicitudes.html', {'solicitudes': solicitudes})


def detalle_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id, usuario=request.user)

    respuestas = solicitud.respuestas.all()
    seguimientos = SeguimientoSolicitud.objects.filter(solicitud=solicitud).order_by('-fecha_creacion')

    return render(request, 'alumno/detalle_solicitud.html', {
        'solicitud': solicitud,
        'respuestas': respuestas,
        'seguimientos': seguimientos
    })