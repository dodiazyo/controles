from django.db import models
from django.core.validators import FileExtensionValidator
from datetime import date, timedelta

# Modelo de Oficiales
class Oficial(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=11)
    cargo = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, choices=[
        ("instalado", "Instalado"),
        ("disponible", "Disponible"),
        ("ausente", "Ausente"),
        ("licencia", "Licencia"),
        ("transferido", "Transferido"),
    ])
    fecha_ingreso = models.DateField()

    def __str__(self):
        return self.nombre

# Modelo de Armas
class Arma(models.Model):
    TIPOS_ARMA = [
        ("pistola", "Pistola"),
        ("escopeta", "Escopeta"),
        ("taser", "Taser"),
        ("otra", "Otra"),
    ]

    ESTADOS = [
        ("disponible", "Disponible"),
        ("asignada", "Asignada"),
        ("fija", "Fija en puesto"),
        ("devuelta", "Devuelta a almacén"),
    ]

    serial = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_ARMA)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="disponible")
    transferida = models.BooleanField(default=False)
    almacen_actual = models.CharField(max_length=100, default="Principal")
    asignada_a = models.ForeignKey("Oficial", on_delete=models.SET_NULL, null=True, blank=True)
    fija_en_puesto = models.BooleanField(default=False)
    fecha_asignacion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    licencia_digital = models.FileField(
        upload_to='licencias_armas/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])]
    )
    fecha_vencimiento_licencia = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"ARM-{self.id:04d} | {self.serial}"

    @property
    def codigo_arma(self):
        return f"ARM-{self.id:04d}"

    @property
    def vence_pronto(self):
        if self.fecha_vencimiento_licencia:
            return self.fecha_vencimiento_licencia <= date.today() + timedelta(days=30)
        return False

# Modelo de Artículos del Inventario
class ArticuloInventario(models.Model):
    CATEGORIAS = [
        ("uniforme", "Uniforme"),
        ("municion", "Munición"),
        ("radio", "Radio de comunicación"),
        ("otro", "Otro"),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    descripcion = models.TextField(blank=True)
    cantidad_total = models.PositiveIntegerField(default=0)
    cantidad_disponible = models.PositiveIntegerField(default=0)
    unidad = models.CharField(max_length=20, default="unidad")
    serial = models.CharField(max_length=50, blank=True, null=True)
    talla = models.CharField(max_length=10, blank=True, null=True)
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"

class UniformeAsignado(models.Model):
    ESTADOS = [
        ("entregado", "Entregado"),
        ("devuelto", "Devuelto"),
        ("deteriorado", "Deteriorado"),
        ("perdido", "Perdido"),
    ]

    oficial = models.ForeignKey(Oficial, on_delete=models.CASCADE)
    articulo = models.ForeignKey(ArticuloInventario, on_delete=models.CASCADE)
    talla = models.CharField(max_length=10, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    fecha_entrega = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.articulo.nombre} asignado a {self.oficial.nombre}"

# Modelo de movimientos del inventario
class MovimientoInventario(models.Model):
    TIPOS_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    articulo = models.ForeignKey(ArticuloInventario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add=True)
    responsable = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo.title()} - {self.articulo.nombre} ({self.cantidad})"

    def save(self, *args, **kwargs):
        if self.tipo == 'entrada':
            self.articulo.cantidad_total += self.cantidad
            self.articulo.cantidad_disponible += self.cantidad
        elif self.tipo == 'salida':
            self.articulo.cantidad_disponible -= self.cantidad
        self.articulo.save()
        super().save(*args, **kwargs)

# Modelo de movimiento de armas
class MovimientoArma(models.Model):
    TIPOS = [
        ('entrega', 'Entrega'),
        ('devolucion', 'Devolución'),
        ('transferencia', 'Transferencia'),
    ]

    arma = models.ForeignKey(Arma, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    oficial = models.ForeignKey("Oficial", on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo.title()} - {self.arma.serial} - {self.fecha}"

    def save(self, *args, **kwargs):
        if self.tipo == 'entrega' and self.oficial:
            self.arma.estado = 'asignada'
            self.arma.asignada_a = self.oficial
        elif self.tipo == 'devolucion':
            self.arma.estado = 'devuelta'
            self.arma.asignada_a = None
        elif self.tipo == 'transferencia':
            self.arma.transferida = True
        self.arma.save()
        super().save(*args, **kwargs)

# MODELOS DE VEHÍCULOS
class Vehiculo(models.Model):
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    tipo = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)
    kilometraje = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.placa

class ChequeoDiario(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    imagen_1 = models.ImageField(upload_to='chequeos/', blank=True, null=True)
    imagen_2 = models.ImageField(upload_to='chequeos/', blank=True, null=True)

    def __str__(self):
        return f"Chequeo {self.fecha} - {self.vehiculo.placa}"

class MantenimientoVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_mantenimiento = models.DateField()
    tipo_mantenimiento = models.CharField(max_length=100)
    kilometraje = models.PositiveIntegerField()
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vehiculo.placa} - {self.tipo_mantenimiento} ({self.fecha_mantenimiento})"

class DocumentoVehiculo(models.Model):
    TIPOS = [
        ("placa", "Placa"),
        ("seguro", "Seguro"),
    ]
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    archivo = models.FileField(upload_to='documentos_vehiculo/', validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])
    fecha_vencimiento = models.DateField()

    def __str__(self):
        return f"{self.tipo} - {self.vehiculo.placa}"

class AsignacionVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Oficial, on_delete=models.SET_NULL, null=True)
    zona = models.CharField(max_length=50)
    fecha_asignacion = models.DateField(auto_now_add=True)
    licencia_supervisor = models.FileField(upload_to='licencias_supervisores/', blank=True, null=True, validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg'])])
    fecha_vencimiento_licencia = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.vehiculo.placa} → {self.supervisor.nombre}"

class CargaCombustible(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    kilometraje_inicial = models.PositiveIntegerField()
    kilometraje_final = models.PositiveIntegerField()
    galones_cargados = models.DecimalField(max_digits=6, decimal_places=2)
    precio_por_galon = models.DecimalField(max_digits=6, decimal_places=2)
    observaciones = models.TextField(blank=True)

    @property
    def kilometros_recorridos(self):
        return self.kilometraje_final - self.kilometraje_inicial

    @property
    def rendimiento_km_por_galon(self):
        if self.galones_cargados > 0:
            return round(self.kilometros_recorridos / float(self.galones_cargados), 2)
        return 0

    @property
    def costo_total(self):
        return round(float(self.galones_cargados) * float(self.precio_por_galon), 2)

    def __str__(self):
        return f"{self.vehiculo.placa} - {self.fecha}"
