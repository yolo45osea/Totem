from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class ZonaViaje(models.Model):
    idZona = models.IntegerField(primary_key=True, verbose_name = "Id Zona")
    nombreZona = models.CharField(max_length=20, verbose_name = "Nombre Zona")

    def __str__(self):
        return self.nombreZona

#----------------------------------------------------------------------------------------------------------------------

# Create your models here.
class Comuna(models.Model):
    idComuna = models.CharField(max_length=5, primary_key=True, verbose_name="Id Comuna")
    nombreComuna = models.CharField(max_length=20, verbose_name = "Nombre Comuna")
    ZonaViaje = models.ForeignKey('ZonaViaje', on_delete=models.CASCADE, verbose_name="Zona Viaje")

    def __str__(self):
        return self.idComuna

#----------------------------------------------------------------------------------------------------------------------

class Vehiculo(models.Model):
    idVehiculo = models.CharField(max_length=5, primary_key=True, verbose_name="Id Vehiculo")
    marcaVehiculo = models.CharField(max_length=20, verbose_name = "Marca Vehiculo")
    modeloVehiculo = models.CharField(max_length=20, verbose_name = "Modelo Vehiculo")
    patenteVehiculo = models.CharField(max_length=20, verbose_name = "Patente Vehiculo")
    FotoVehiculo = models.ImageField(upload_to="imagenes",null=True, verbose_name="Foto Vehiculo")

    def __str__(self):
        return self.idVehiculo
    
#----------------------------------------------------------------------------------------------------------------------

# Create your models here.
class Sector(models.Model):
    idSector = models.CharField(max_length=5, primary_key=True, verbose_name="Id Sector")
    nombreSector = models.CharField(max_length=255, verbose_name = "Nombre Sector")

    def __str__(self):
        return self.idSector

#----------------------------------------------------------------------------------------------------------------------

class Chofer(models.Model):
    idChofer = models.CharField(max_length=5, primary_key=True, verbose_name="Id Chofer")
    nombreChofer = models.CharField(max_length=30, verbose_name = "Nombre Chofer")
    email = models.EmailField(max_length=254, unique=True, verbose_name="Correo Electrónico")
    rut = models.CharField(max_length=10, verbose_name="Rut del Chofer")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    activo = models.BooleanField(default=True, verbose_name="¿Está Activo?")
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, related_name='Vehiculo')
    cupos = models.PositiveIntegerField(verbose_name="Cupos")
    horario1 = models.TimeField(verbose_name="Horario 1")
    horario2 = models.TimeField(verbose_name="Horario 2")
    horario3 = models.TimeField(verbose_name="Horario 3")
    FotoPerfil = models.ImageField(upload_to="imagenes",null=True, verbose_name="Foto Perfil")
    destino = models.ForeignKey('Comuna', on_delete=models.CASCADE, related_name='Comuna')
    fechaRegistro = models.DateField(null=True, verbose_name="Fecha Registro")
    ubicacion = models.ForeignKey('Sector', on_delete=models.CASCADE, related_name='Sector')


    def set_password(self, raw_password):
        """Encripta y guarda la contraseña."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verifica si la contraseña ingresada es correcta."""
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.nombreChofer
#----------------------------------------------------------------------------------------------------------------------

class MetodoPago(models.Model):
    idPago = models.CharField(max_length=5, primary_key=True, verbose_name="Id Pago")
    nombre = models.CharField(max_length=50, verbose_name="Nombre Pago")  # Ej. Tarjeta de crédito, PayPal
    tipo = models.ForeignKey('Tipo', on_delete=models.CASCADE, related_name='Tipo')  # Cambié related_name aquí
    numero = models.CharField(max_length=20, blank=True, verbose_name="Número de Cuenta o Tarjeta")
    pasajero = models.ForeignKey('Pasajero', on_delete=models.CASCADE, related_name='metodos_pago_pasajero')  # Cambié related_name aquí

    def __str__(self):
        return self.idPago
    
#----------------------------------------------------------------------------------------------------------------------

class Tipo(models.Model):
    idTipo = models.CharField(max_length=5, primary_key=True, verbose_name="Id Tipo")
    nombre = models.CharField(max_length=50, verbose_name="Nombre Tipo")  # Ej. Tarjeta de crédito, PayPal

    def __str__(self):
        return self.idTipo


#----------------------------------------------------------------------------------------------------------------------
class Pasajero(models.Model):
    idPasajero = models.CharField(max_length=5, primary_key=True, verbose_name="Id Pasajero")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Pasajero")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    rut = models.CharField(max_length=10, verbose_name="Rut del Pasajero")

    def __str__(self):
        return self.idPasajero
    
"""class Calificacion(models.Model):
    id"""

class Reserva(models.Model):
    idReserva = models.CharField(max_length=5, primary_key=True, verbose_name="Id Reserva")
    fecha = models.DateField(null=True, verbose_name="Fecha")
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, related_name='vehiculo_reservado')
    estado = models.BooleanField(default=True, verbose_name="Estado")
    estadoTexto = models.CharField(max_length=5, verbose_name="Estado Texto")
    pasajero = models.ForeignKey('Pasajero', on_delete=models.CASCADE, related_name='Pasajero')
    horario = models.TimeField(verbose_name="Horario")
    chofer = models.ForeignKey('Chofer', on_delete=models.CASCADE, related_name='Chofer')
    calificacion = models.PositiveIntegerField(default=0, verbose_name="Calificacion")
    resena = models.CharField(max_length=255, verbose_name="Reseña")
    respuesta = models.CharField(max_length=255, verbose_name="Respuesta")

    nombreAcompanante1 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre del Acompañante 1")
    emailAcompanante1 = models.EmailField(null=True, blank=True, verbose_name="Correo Electrónico del Acompañante 1")
    rutAcompanante1 = models.CharField(max_length=10, null=True, blank=True, verbose_name="Rut del Acompañante 1")

    nombreAcompanante2 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre del Acompañante 2")
    emailAcompanante2 = models.EmailField(null=True, blank=True, verbose_name="Correo Electrónico del Acompañante 2")
    rutAcompanante2 = models.CharField(max_length=10, null=True, blank=True, verbose_name="Rut del Acompañante 2")

    nombreAcompanante3 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre del Acompañante 3")
    emailAcompanante3 = models.EmailField(null=True, blank=True, verbose_name="Correo Electrónico del Acompañante 3")
    rutAcompanante3 = models.CharField(max_length=10, null=True, blank=True, verbose_name="Rut del Acompañante 3")

    def __str__(self):
        return self.idReserva
    

class TipoAdmin(models.Model):
    idTipo = models.CharField(max_length=5, primary_key=True, verbose_name="Id Tipo Admin")
    nombre = models.CharField(max_length=50, verbose_name="Nombre Tipo Admin")

    def __str__(self):
        return self.idTipo
    
class Admin(models.Model):
    idAdmin = models.CharField(max_length=5, primary_key=True, verbose_name="Id Admin")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Admin")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    rut = models.CharField(max_length=10, verbose_name="Rut del Admin")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    tipo = models.ForeignKey('TipoAdmin', on_delete=models.CASCADE, related_name='Tipo_Admin')  # Cambié related_name aquí
    activo = models.BooleanField(default=True, verbose_name="¿Está Activo?")
    fechaRegistro = models.DateField(null=True, verbose_name="Fecha Registro")


    def set_password(self, raw_password):
        """Encripta y guarda la contraseña."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verifica si la contraseña ingresada es correcta."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.idAdmin



class Totem(models.Model):
    idTotem = models.CharField(max_length=5, primary_key=True, verbose_name="Id Totem")
    ip = models.CharField(max_length=50, verbose_name="IP")
    serie = models.CharField(max_length=50, verbose_name="Serie")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    ubicacion = models.CharField(max_length=50, verbose_name="Ubicación")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    fecha = models.DateField(null=True, verbose_name="Fecha")

    def __str__(self):
        return self.idTotem
