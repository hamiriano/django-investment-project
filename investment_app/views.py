from django.shortcuts import render, redirect
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
from django.db import transaction
from django.contrib import messages

def index(request):
    return render(request, 'investment_app/index.html')
# ViewSet para el modelo Activo
class ActivoViewSet(viewsets.ModelViewSet):
    queryset = Activo.objects.all()
    serializer_class = ActivoSerializer

# ViewSet para el modelo Portafolio
class PortafolioViewSet(viewsets.ModelViewSet):
    queryset = Portafolio.objects.all()
    serializer_class = PortafolioSerializer

# ViewSet para el modelo Precio
class PrecioViewSet(viewsets.ModelViewSet):
    queryset = Precio.objects.all()
    serializer_class = PrecioSerializer

# ViewSet para el modelo Cantidad
class CantidadViewSet(viewsets.ModelViewSet):
    queryset = Cantidad.objects.all()
    serializer_class = CantidadSerializer

# ViewSet para el modelo Weight
class WeightViewSet(viewsets.ModelViewSet):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer


# APIView para obtener el valor del portafolio en un rango de fechas
class PortfolioValueDetail(APIView):
    def get(self, request, portafolio_id):
        # Obtener las fechas de inicio y fin de los parámetros de la solicitud
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        
        # Obtener el portafolio por ID, o devolver un 404 si no existe
        portafolio = get_object_or_404(Portafolio, id=portafolio_id)
        
        # Obtener los precios en el rango de fechas especificado
        precios = Precio.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        
        # Obtener las cantidades del portafolio
        cantidades = Cantidad.objects.filter(portafolio=portafolio)
        
        # Calcular el valor del portafolio por fecha
        valores_por_fecha = {}
        for precio in precios:
            fecha = precio.fecha
            if fecha not in valores_por_fecha:
                valores_por_fecha[fecha] = 0
            try:
                cantidad = cantidades.get(activo=precio.activo).cantidad
                valores_por_fecha[fecha] += precio.valor * cantidad
            except Cantidad.DoesNotExist:
                # Manejar el caso en que no se encuentra la cantidad para el activo
                valores_por_fecha[fecha] += 0
        
        # Preparar los datos de respuesta
        response_data = {
            'valores_por_fecha': valores_por_fecha
        }
        
        # Renderizar la plantilla con los datos de respuesta
        return render(request, 'investment_app/portfolio_values.html', response_data)
    
# APIView para obtener los pesos del portafolio
class PortfolioWeightDetail(APIView):
    def get(self, request, portafolio_id):
        # Obtener el portafolio por ID, o devolver un 404 si no existe
        portafolio = get_object_or_404(Portafolio, id=portafolio_id)
        
        # Obtener los pesos del portafolio
        weights = Weight.objects.filter(portafolio=portafolio)
        
        # Serializar los datos de los pesos
        serializer = WeightSerializer(weights, many=True)
        
        # Renderizar la plantilla con los datos de los pesos
        return render(request, 'investment_app/portfolio_weights.html', {'weights': weights})

# APIView para listar todos los pesos
class WeightList(APIView):
    def get(self, request):
        # Obtener todos los pesos
        weights = Weight.objects.all()
        
        # Renderizar la plantilla con los datos de los pesos
        return render(request, 'investment_app/portfolio_weights.html', {'weights': weights})
    
# APIView para listar todos los precios
class PriceList(APIView):
    def get(self, request):
        # Obtener todos los precios
        precios = Precio.objects.all()
        
        # Renderizar la plantilla con los datos de los precios
        return render(request, 'investment_app/portfolio_prices.html', {'precios': precios})
    
# APIView para listar todas las cantidades iniciales
class CantidadList(APIView):
    def get(self, request):
        # Obtener todas las cantidades
        cantidades = Cantidad.objects.all()
        
        # Agrupar las cantidades por portafolio
        portafolio_1_cantidades = cantidades.filter(portafolio__id=1)
        portafolio_2_cantidades = cantidades.filter(portafolio__id=2)
        
        # Renderizar la plantilla con los datos de las cantidades
        return render(request, 'investment_app/portfolio_cantidades.html', {
            'portafolio_1_cantidades': portafolio_1_cantidades,
            'portafolio_2_cantidades': portafolio_2_cantidades
        })


@api_view(['GET', 'POST'])
def cargar_datos(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            file_name = 'datos.xlsx'  # Nombre fijo para el archivo
            file_path = default_storage.save(file_name, ContentFile(file.read()))
            
            # Leer el archivo Excel
            xls = pd.ExcelFile(file_path)
            
            with transaction.atomic():
                # Limpiar las tablas relevantes
                Activo.objects.all().delete()
                Portafolio.objects.all().delete()
                Precio.objects.all().delete()
                Cantidad.objects.all().delete()
                Weight.objects.all().delete()
                
                # Crear los portafolios si no existen
                portafolio_1, created = Portafolio.objects.get_or_create(id=1, defaults={'nombre': 'Portafolio 1', 'valor_inicial': 1000000000})
                portafolio_2, created = Portafolio.objects.get_or_create(id=2, defaults={'nombre': 'Portafolio 2', 'valor_inicial': 1000000000})
                
                # Cargar datos de la hoja Weights
                df_weights = pd.read_excel(xls, 'weights')
                activos = {}
                weights = []
                for index, row in df_weights.iterrows():
                    activo, created = Activo.objects.get_or_create(nombre=row['activos'], defaults={'precio': 0})
                    activos[row['activos']] = activo
                    weights.append(Weight(portafolio=portafolio_1, activo=activo, peso=row['portafolio 1']))
                    weights.append(Weight(portafolio=portafolio_2, activo=activo, peso=row['portafolio 2']))
                Weight.objects.bulk_create(weights)
                
                # Cargar datos de la hoja Precios
                df_precios = pd.read_excel(xls, 'Precios')
                precios = []
                for index, row in df_precios.iterrows():
                    fecha = row['Dates']
                    for activo_nombre in df_precios.columns[1:]:
                        activo = activos[activo_nombre]
                        precios.append(Precio(activo=activo, fecha=fecha, valor=row[activo_nombre]))
                Precio.objects.bulk_create(precios)
                
                # Calcular y guardar las cantidades iniciales
                valor_inicial = 1000000000
                cantidades = []
                for index, row in df_weights.iterrows():
                    activo = activos[row['activos']]
                    peso_1 = float(row['portafolio 1'])
                    peso_2 = float(row['portafolio 2'])
                    precio_inicial = float(Precio.objects.get(activo=activo, fecha='2022-02-15').valor)
                    cantidad_1 = (peso_1 * valor_inicial) / precio_inicial
                    cantidad_2 = (peso_2 * valor_inicial) / precio_inicial
                    cantidades.append(Cantidad(portafolio=portafolio_1, activo=activo, cantidad=cantidad_1))
                    cantidades.append(Cantidad(portafolio=portafolio_2, activo=activo, cantidad=cantidad_2))
                Cantidad.objects.bulk_create(cantidades)
            
            messages.success(request, "Datos cargados correctamente")
            return redirect('cargar-datos')
        
        except Exception as e:
            logger.error(f"Error al cargar datos: {e}")
            messages.error(request, f"Error al cargar datos: {e}")
            return redirect('cargar-datos')
    
    # Renderizar la plantilla para la solicitud GET
    if request.method == 'GET':
        return render(request, 'investment_app/cargar_datos.html')
    
logger = logging.getLogger(__name__)