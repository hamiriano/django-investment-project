from django.test import TestCase
from .models import Activo, Portafolio, Precio, Cantidad, Weight

class InvestmentAppTests(TestCase):

    def setUp(self):
        # Create test data for Activos, Portafolios, Precios, Cantidades, and Weights
        self.portafolio1 = Portafolio.objects.create(nombre="Portafolio 1")
        self.portafolio2 = Portafolio.objects.create(nombre="Portafolio 2")
        
        self.activo1 = Activo.objects.create(nombre="EEUU")
        self.activo2 = Activo.objects.create(nombre="Europa")
        
        self.precio1 = Precio.objects.create(activo=self.activo1, valor=9383.57, fecha="2022-02-15")
        self.precio2 = Precio.objects.create(activo=self.activo2, valor=66.03, fecha="2022-02-15")
        
        self.cantidad1 = Cantidad.objects.create(activo=self.activo1, portafolio=self.portafolio1, cantidad=0)
        self.cantidad2 = Cantidad.objects.create(activo=self.activo2, portafolio=self.portafolio2, cantidad=0)
        
        self.weight1 = Weight.objects.create(activo=self.activo1, portafolio=self.portafolio1, peso=0.28)
        self.weight2 = Weight.objects.create(activo=self.activo2, portafolio=self.portafolio2, peso=0.087)

    def test_portafolio_creation(self):
        self.assertEqual(self.portafolio1.nombre, "Portafolio 1")
        self.assertEqual(self.portafolio2.nombre, "Portafolio 2")

    def test_activo_creation(self):
        self.assertEqual(self.activo1.nombre, "EEUU")
        self.assertEqual(self.activo2.nombre, "Europa")

    def test_precio_creation(self):
        self.assertEqual(self.precio1.valor, 9383.57)
        self.assertEqual(self.precio2.valor, 66.03)

    def test_cantidad_creation(self):
        self.assertEqual(self.cantidad1.cantidad, 0)
        self.assertEqual(self.cantidad2.cantidad, 0)

    def test_weight_creation(self):
        self.assertEqual(self.weight1.peso, 0.28)
        self.assertEqual(self.weight2.peso, 0.087)