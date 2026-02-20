from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestor.views import *
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'alumnos', AlumnoViewSet)
router.register(r'recursos', RecursoViewSet)
router.register(r'solicitudes', SolicitudViewSet)
router.register(r'detalles', DetalleSolicitudViewSet)
router.register(r'prestamos', PrestamoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Asegúrate de que esta sea la ÚNICA ruta de token
    path('api/token/', MyTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/', include(router.urls)),
]