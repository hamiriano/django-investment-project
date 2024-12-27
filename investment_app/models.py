from django.db import models

class Activo(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.nombre

class Portafolio(models.Model):
    nombre = models.CharField(max_length=100)
    valor_inicial = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.nombre

class Precio(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, related_name='precios')
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = ('activo', 'fecha')

class Cantidad(models.Model):
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = ('portafolio', 'activo')

class Weight(models.Model):
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        unique_together = ('portafolio', 'activo')

class Monto(models.Model):
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = ('portafolio', 'activo', 'fecha')