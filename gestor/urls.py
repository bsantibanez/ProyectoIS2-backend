# gestor/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecursoViewSet  # Asegúrate de importar tus otros ViewSets aquí

router = DefaultRouter()
router.register(r'recursos', RecursoViewSet)
# router.register(r'alumnos', AlumnoViewSet) # Ejemplo para cuando los tengas

urlpatterns = [
    path('', include(router.urls)),
]