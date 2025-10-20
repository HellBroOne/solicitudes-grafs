from django.db import models


class TipoSolicitud(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=350)

    def __str__(self):
        return self.nombre
