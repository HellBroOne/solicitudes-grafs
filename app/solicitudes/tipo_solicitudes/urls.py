from django.urls import path
from tipo_solicitudes import views

'tipo-solicitud/'
urlpatterns = [
    path('nuevo/', views.agregar, name='agrega_solicitud'),
    path('lista/', views.lista_solicitudes, name='lista_tipo_solicitudes'),
    path('crear/<int:tipo_id>/', views.crear_solicitud, name='crear_solicitud'),
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('solicitud/<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'),
]
