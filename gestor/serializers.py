from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# --- SERIALIZADOR DE TOKEN (JWT CUSTOM) ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # 1. Django espera 'username', nosotros le pasamos el 'email'
        attrs['username'] = attrs.get('email')
    
        # 2. Obtenemos la respuesta estándar (que trae 'access' y 'refresh')
        data = super().validate(attrs)
        
        # 3. AGREGAMOS EL ROL AQUÍ (Esto es lo que Angular leerá como res.rol)
        data['rol'] = self.user.rol 
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Esto lo dejamos igual por seguridad (dentro del token payload)
        token['rol'] = user.rol 
        token['email'] = user.email
        return token
    

# --- SERIALIZADORES DE MODELOS ---

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol']

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = ['id', 'estado']

class DetalleSolicitudSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo intermedio. 
    Se mantiene para el ViewSet independiente de detalles.
    """
    class Meta:
        model = DetalleSolicitud
        fields = ['id', 'solicitud', 'recurso']

class SolicitudSerializer(serializers.ModelSerializer):
    """
    Serializador de Solicitud actualizado para mostrar una lista 
    de recursos en lugar de uno solo.
    """
    # 'recursos' utiliza el related_name='detalles' definido en el modelo DetalleSolicitud
    recursos = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='recurso_id', # Muestra el ID del recurso (ej: 'L-01')
        source='detalles'        # Origen de los datos
    )

    class Meta:
        model = Solicitud
        # Importante: se eliminó 'recurso' y se agregó 'recursos'
        fields = [
            'id', 
            'usuario', 
            'alumno', 
            'recursos', 
            'motivo', 
            'estado', 
            'fecha_solicitud'
        ]

class PrestamoSerializer(serializers.ModelSerializer):
    solicitud = SolicitudSerializer(read_only=True)

    class Meta:
        model = Prestamo
        fields = [
            'id', 
            'solicitud', 
            'fecha_entrega', 
            'fecha_devolucion', 
            'estado'
        ]