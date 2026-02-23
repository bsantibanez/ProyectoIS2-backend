from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Usuario personalizado con Roles
class Usuario(AbstractUser):
    # 0: Ayudante, 1: Autoridad Académica
    rol = models.IntegerField(default=0) 
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# 2. Alumno
class Alumno(models.Model):
    rut = models.CharField(max_length=12, primary_key=True) # Tú lo ingresas manualmente
    nombre = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.nombre} ({self.rut})"

# 3. Recurso
class Recurso(models.Model):
    id = models.CharField(max_length=50, primary_key=True) # ID String como pediste
    estado = models.CharField(max_length=20, default='Disponible')
    def __str__(self):
        return self.id

# 4. Solicitud
class Solicitud(models.Model):
    ESTADOS = (('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada'))
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) # El ayudante que la crea
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    motivo = models.TextField()
    
# 5. Detalle de Solicitud
class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, related_name='detalles', on_delete=models.CASCADE)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)

# 6. Prestamo (Relación OneToOne con Solicitud)
class Prestamo(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    fecha_entrega = models.DateTimeField()
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20)