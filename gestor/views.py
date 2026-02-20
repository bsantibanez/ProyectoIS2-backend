from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication # Importación correcta
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

# --- VIEWSETS ---

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAutoridadAcademica]

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    # Usamos JWT para evitar el error 'AttributeError: Token'
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

class DetalleSolicitudViewSet(viewsets.ModelViewSet):
    queryset = DetalleSolicitud.objects.all()
    serializer_class = DetalleSolicitudSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]