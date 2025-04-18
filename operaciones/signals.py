from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MovimientoInventario

@receiver(post_save, sender=MovimientoInventario)
def actualizar_stock(sender, instance, **kwargs):
    articulo = instance.articulo
    if instance.tipo == "entrada":
        articulo.cantidad_disponible += instance.cantidad
    elif instance.tipo == "salida":
        articulo.cantidad_disponible -= instance.cantidad
    articulo.save()
from .models import MovimientoArma

@receiver(post_save, sender=MovimientoArma)
def actualizar_estado_arma(sender, instance, **kwargs):
    arma = instance.arma
    if instance.tipo == "asignación":
        arma.estado = "asignada"
        arma.asignada_a = instance.oficial
        arma.almacen_actual = None
    elif instance.tipo == "devolución":
        arma.estado = "disponible"
        arma.asignada_a = None
        arma.almacen_actual = "Almacén Principal"
    arma.save()
