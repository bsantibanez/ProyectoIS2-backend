from urllib import request

from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter, CharFilter
from django.db import transaction 
from django.utils import timezone
from urllib3 import request  # Necesario para timezone.now()

from .models import *
from .serializers import *
from .serializers import MyTokenObtainPairSerializer

# --- VISTA DE LOGIN (JWT) ---
class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print("\n--- DATOS RECIBIDOS DESDE EL FRONT ---")
        print(f"Cuerpo: {request.data}")
        print("--------------------------------------\n")
        return super().post(request, *args, **kwargs)

# --- PERMISOS ---
class IsAutoridadAcademica(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 1

# --- FILTROS ---
class PrestamoFilter(FilterSet):
    # Definimos rangos para las fechas
    fecha_desde = DateTimeFilter(field_name="fecha_entrega", lookup_expr='gte')
    fecha_hasta = DateTimeFilter(field_name="fecha_entrega", lookup_expr='lte')
    alumno_rut = CharFilter(field_name="solicitud__alumno__rut", lookup_expr='icontains')

    class Meta:
        model = Prestamo
        fields = ['estado', 'fecha_desde', 'fecha_hasta', 'alumno_rut']

# --- VIEWSETS ---

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAutoridadAcademica]

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # --- MÉTODO PARA CREAR (Se mantiene tu lógica original) ---
    def create(self, request, *args, **kwargs):
        data = request.data
        with transaction.atomic():
            try:
                alumno_instancia = Alumno.objects.get(rut=data.get('alumno'))
                usuario_instancia = Usuario.objects.get(id=data.get('usuario'))
            except (Alumno.DoesNotExist, Usuario.DoesNotExist) as e:
                return Response({"error": "Alumno o Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

            solicitud = Solicitud.objects.create(
                alumno=alumno_instancia,
                usuario=usuario_instancia,
                motivo=data.get('motivo', ''),
                estado='Pendiente'
            )
            
            recursos_ids = data.get('recursos', [])
            if not recursos_ids:
                transaction.set_rollback(True) 
                return Response({"error": "Debe seleccionar al menos un recurso"}, status=status.HTTP_400_BAD_REQUEST)

            for r_id in recursos_ids:
                recurso_obj = Recurso.objects.get(id=r_id)
                DetalleSolicitud.objects.create(solicitud=solicitud, recurso=recurso_obj)
                recurso_obj.estado = 'En Solicitud'
                recurso_obj.save()

            serializer = self.get_serializer(solicitud)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # --- APROBAR Y CREAR PRÉSTAMO ---
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        nuevo_estado = request.data.get('estado')

        with transaction.atomic():
            # 1. Definimos los detalles ANTES de los IF para que ambos casos los vean
            detalles = DetalleSolicitud.objects.filter(solicitud=instance)

            if nuevo_estado == 'Aprobada' and instance.estado != 'Aprobada':
                Prestamo.objects.create(
                    solicitud=instance,
                    fecha_entrega=timezone.now(),
                    estado='En Curso'
                )
                
                for detalle in detalles:
                    recurso = detalle.recurso
                    recurso.estado = 'En Préstamo'
                    recurso.save()
                    
            elif nuevo_estado == 'Rechazada':
                # 2. Ahora 'detalles' sí existe aquí
                for detalle in detalles:
                    recurso = detalle.recurso
                    recurso.estado = 'Disponible'
                    recurso.save()

            # 3. No olvides guardar el nuevo estado de la solicitud misma
            instance.estado = nuevo_estado
            instance.save()

        return super().partial_update(request, *args, **kwargs)

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    # Integración de Filtros
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrestamoFilter

    def get_queryset(self):
        # Optimizamos la consulta para traer datos del alumno y solicitud en un solo viaje
        return Prestamo.objects.select_related('solicitud', 'solicitud__alumno').all()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        nuevo_estado = request.data.get('estado')

        if nuevo_estado == 'Finalizado':
            with transaction.atomic():
                instance.fecha_devolucion = timezone.now()
                instance.estado = 'Finalizado'
                instance.save()
                
                # Liberar recursos y actualizar solicitud
                detalles = DetalleSolicitud.objects.filter(solicitud=instance.solicitud)
                for d in detalles:
                    d.recurso.estado = 'Disponible'
                    d.recurso.save()
                
                instance.solicitud.estado = 'Finalizada'
                instance.solicitud.save()

        return super().partial_update(request, *args, **kwargs)

class DetalleSolicitudViewSet(viewsets.ModelViewSet):
    queryset = DetalleSolicitud.objects.all()
    serializer_class = DetalleSolicitudSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]