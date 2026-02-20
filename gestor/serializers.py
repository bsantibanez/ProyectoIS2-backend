from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        # Esto lo dejamos igual por seguridad (dentro del token)
        token['rol'] = user.rol 
        token['email'] = user.email
        return token
    

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

# serializers.py en Django
class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['id', 'usuario', 'alumno', 'recurso', 'motivo', 'estado', 'fecha_solicitud']

class DetalleSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleSolicitud
        fields = '__all__'

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'