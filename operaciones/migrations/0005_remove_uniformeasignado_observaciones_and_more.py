# Generated by Django 5.2 on 2025-04-18 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operaciones', '0004_uniformeasignado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uniformeasignado',
            name='observaciones',
        ),
        migrations.AlterField(
            model_name='uniformeasignado',
            name='articulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operaciones.articuloinventario'),
        ),
        migrations.AlterField(
            model_name='uniformeasignado',
            name='estado',
            field=models.CharField(choices=[('entregado', 'Entregado'), ('devuelto', 'Devuelto'), ('deteriorado', 'Deteriorado'), ('perdido', 'Perdido')], max_length=20),
        ),
    ]
