from django.shortcuts import render
from rest_framework import viewsets
from .models import Activo, Portafolio, Precio, Cantidad, Weight
from .serializers import ActivoSerializer, PortafolioSerializer, PrecioSerializer, CantidadSerializer, WeightSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import F
import pandas as pd
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser
import logging

class ActivoViewSet(viewsets.ModelViewSet):
    queryset = Activo.objects.all()
    serializer_class = ActivoSerializer

class PortafolioViewSet(viewsets.ModelViewSet):
    queryset = Portafolio.objects.all()
    serializer_class = PortafolioSerializer

class PrecioViewSet(viewsets.ModelViewSet):
    queryset = Precio.objects.all()
    serializer_class = PrecioSerializer

class CantidadViewSet(viewsets.ModelViewSet):
    queryset = Cantidad.objects.all()
    serializer_class = CantidadSerializer

class WeightViewSet(viewsets.ModelViewSet):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer

def index(request):
    return render(request, 'investment_app/index.html')

class PortfolioValueDetail(APIView):
    def get(self, request, portafolio_id):
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        
        portafolio = get_object_or_404(Portafolio, id=portafolio_id)
        precios = Precio.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        cantidades = Cantidad.objects.filter(portafolio=portafolio)
        
        valores_por_fecha = {}
        for precio in precios:
            fecha = precio.fecha
            if fecha not in valores_por_fecha:
                valores_por_fecha[fecha] = 0
            cantidad = cantidades.get(activo=precio.activo).cantidad
            valores_por_fecha[fecha] += precio.valor * cantidad
        
        response_data = {
            'valores_por_fecha': valores_por_fecha
        }
        
        return render(request, 'investment_app/portfolio_values.html', response_data)
    
class PortfolioWeightDetail(APIView):
    def get(self, request, portafolio_id):
        portafolio = get_object_or_404(Portafolio, id=portafolio_id)
        weights = Weight.objects.filter(portafolio=portafolio)
        serializer = WeightSerializer(weights, many=True)
        return render(request, 'investment_app/portfolio_weights.html', {'weights': weights})

class WeightList(APIView):
    def get(self, request):
        weights = Weight.objects.all()
        serializer = WeightSerializer(weights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PriceList(APIView):
    def get(self, request):
        precios = Precio.objects.all()
        serializer = PrecioSerializer(precios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def cargar_datos(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            file_name = 'datos.xlsx'  # Nombre fijo para el archivo
            file_path = default_storage.save(file_name, ContentFile(file.read()))
            
            # Leer el archivo Excel
            xls = pd.ExcelFile(file_path)
            
            # Crear los portafolios si no existen
            portafolio_1, created = Portafolio.objects.get_or_create(id=1, defaults={'nombre': 'Portafolio 1', 'valor_inicial': 1000000000})
            portafolio_2, created = Portafolio.objects.get_or_create(id=2, defaults={'nombre': 'Portafolio 2', 'valor_inicial': 1000000000})
            
            # Cargar datos de la hoja Weights
            df_weights = pd.read_excel(xls, 'weights')
            for index, row in df_weights.iterrows():
                activo, created = Activo.objects.get_or_create(nombre=row['activos'], defaults={'precio': 0})
                Weight.objects.update_or_create(portafolio=portafolio_1, activo=activo, defaults={'peso': row['portafolio 1']})
                Weight.objects.update_or_create(portafolio=portafolio_2, activo=activo, defaults={'peso': row['portafolio 2']})
            
            # Cargar datos de la hoja Precios
            df_precios = pd.read_excel(xls, 'Precios')
            for index, row in df_precios.iterrows():
                fecha = row['Dates']
                for activo_nombre in df_precios.columns[1:]:
                    activo = Activo.objects.get(nombre=activo_nombre)
                    Precio.objects.update_or_create(activo=activo, fecha=fecha, defaults={'valor': row[activo_nombre]})
            
            return Response({"status": "Datos cargados correctamente"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Error al cargar datos: {e}")
            return Response({"status": "Error al cargar datos", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Renderizar la plantilla para la solicitud GET
    if request.method == 'GET':
        return render(request, 'investment_app/cargar_datos.html')