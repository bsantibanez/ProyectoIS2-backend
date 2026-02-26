from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    first_name = models.CharField(max_length=150, verbose_name="Nombres")
    last_name = models.CharField(max_length=150, verbose_name="Apellidos")
    rol = models.IntegerField(default=0) 
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'rol']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

# 2. Alumno
class Alumno(models.Model):
    rut = models.CharField(max_length=12, primary_key=True) # Tú lo ingresas manualmente
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"

# 3. Recurso
class Recurso(models.Model):
    id = models.CharField(max_length=50, primary_key=True) # ID String como pediste
    estado = models.CharField(max_length=20, default='Disponible')
    def __str__(self):
        return self.id

# 4. Solicitud
class Solicitud(models.Model):
    estados = (('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada'))
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) 
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=estados, default='Pendiente')
    motivo = models.TextField()
    
# 5. Detalle de Solicitud
class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, related_name='detalles', on_delete=models.CASCADE)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)

# 6. Prestamo (Relación OneToOne con Solicitud)
class Prestamo(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20)