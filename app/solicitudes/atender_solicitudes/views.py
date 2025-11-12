from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from tipo_solicitudes.models import Solicitud, SeguimientoSolicitud, User
from django.contrib.auth.decorators import login_required
# csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import CerrarSolicitudForm

# Se regresa JsonResponse en lugar de redirecciones para facilitar pruebas con herramientas como Postman.
# Debe ser remplazado por redirecciones en producción.

# @login_required
@csrf_exempt
def marcar_solicitud_en_proceso(request, solicitud_id: int):
	if request.method != 'POST':
		messages.error(request, 'Método no permitido.')
		# Línea de template comentada (render formulario)
		# return render(request, 'marcar_en_proceso.html')
		return JsonResponse({'error': 'Metodo no permitido.'}, status=405)
	solicitud = get_object_or_404(Solicitud, id=solicitud_id)
	ultimo = solicitud.seguimientos.order_by('-fecha_creacion').first()
	if not ultimo or ultimo.estatus != '1':
		messages.error(request, 'No se puede cambiar el estatus: la solicitud no está en estado Creada.')
		# return redirect('bienvenida')
		# Regresar JsonResponse por ahora
		return JsonResponse({'error': 'No se puede cambiar el estatus: la solicitud no está en estado Creada.'}, status=400)
	SeguimientoSolicitud.objects.create(solicitud=solicitud, estatus='2', observaciones='')
	messages.success(request, 'La solicitud fue marcada como En proceso.')
	# return redirect('bienvenida')
	# Regresar JsonResponse por ahora
	return JsonResponse({'mensaje': 'La solicitud fue marcada como En proceso.'})

# @login_required
@csrf_exempt
def cerrar_solicitud(request, solicitud_id: int):
	solicitud = get_object_or_404(Solicitud, id=solicitud_id)
	ultimo = solicitud.seguimientos.order_by('-fecha_creacion').first()
	if not ultimo or ultimo.estatus != '2':
		messages.error(request, 'Solo se puede cerrar si está En proceso.')
		# return redirect('bienvenida')
		return JsonResponse({'error': 'Solo se puede cerrar si está En proceso.'}, status=400)
	if request.method != 'POST':
		# Línea de template comentada (render formulario)
		# return render(request, 'cerrar_solicitud.html', {'form': CerrarSolicitudForm()})
		return JsonResponse({'error': 'Método no permitido.'}, status=405)

	form = CerrarSolicitudForm(request.POST)
	if not form.is_valid():
		messages.error(request, 'Formulario inválido. Verifique los datos.')
		# return redirect('bienvenida')
		return JsonResponse({'error': form.errors.as_json()}, status=400)

	estatus = form.cleaned_data['estatus']  # normalizado a '3' o '4'
	observaciones = form.cleaned_data['observaciones'].strip()

	SeguimientoSolicitud.objects.create(
		solicitud=solicitud,
		estatus=estatus,
		observaciones=observaciones
	)
	messages.success(request, 'Solicitud cerrada correctamente.')
	# return redirect('bienvenida')
	return JsonResponse({'mensaje': 'Solicitud cerrada correctamente.', 'estatus': estatus})
