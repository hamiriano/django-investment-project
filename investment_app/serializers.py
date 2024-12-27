from rest_framework import serializers
from .models import Activo, Portafolio, Precio, Cantidad, Weight

class ActivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activo
        fields = '__all__'

class PortafolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portafolio
        fields = '__all__'

class PrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precio
        fields = '__all__'

class CantidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cantidad
        fields = '__all__'

class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = '__all__'

