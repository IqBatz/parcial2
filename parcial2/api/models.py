from django.db import models

# Create your models here.
class Ordenes(models.Model):
    nombreCliente=models.CharField(max_length=500)
    total=models.DecimalField(decimal_places=2,max_digits=10)
    