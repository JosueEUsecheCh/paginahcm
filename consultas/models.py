from django.db import models

class RegistroFamiliar(models.Model):
    ci_titular = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=100)
    nombres = models.CharField(max_length=100)
    ci_beneficiario = models.CharField(max_length=20)
    parentesco = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    discapacidad = models.CharField(max_length=100, blank=True)
    custodia_legal = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.apellidos} {self.nombres} ({self.ci_beneficiario})"
