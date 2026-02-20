from django.contrib import admin
from .models import Usuario, Alumno, Recurso, Solicitud, DetalleSolicitud, Prestamo

admin.site.register(Usuario)
admin.site.register(Alumno)
admin.site.register(Recurso)
admin.site.register(Solicitud)
admin.site.register(DetalleSolicitud)
admin.site.register(Prestamo)
