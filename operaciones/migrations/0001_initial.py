# Generated by Django 5.2 on 2025-04-18 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=50, unique=True)),
                ('tipo', models.CharField(choices=[('pistola', 'Pistola'), ('escopeta', 'Escopeta'), ('taser', 'Taser'), ('otra', 'Otra')], max_length=20)),
                ('estado', models.CharField(choices=[('disponible', 'Disponible'), ('asignada', 'Asignada'), ('fija', 'Fija en puesto'), ('devuelta', 'Devuelta a almacén')], default='disponible', max_length=20)),
                ('transferida', models.BooleanField(default=False)),
                ('almacen_actual', models.CharField(default='Principal', max_length=100)),
                ('fija_en_puesto', models.BooleanField(default=False)),
                ('fecha_asignacion', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArticuloInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.CharField(choices=[('uniforme', 'Uniforme'), ('municion', 'Munición'), ('radio', 'Radio de comunicación'), ('otro', 'Otro')], max_length=20)),
                ('descripcion', models.TextField(blank=True)),
                ('cantidad_total', models.PositiveIntegerField(default=0)),
                ('cantidad_disponible', models.PositiveIntegerField(default=0)),
                ('unidad', models.CharField(default='unidad', max_length=20)),
                ('serial', models.CharField(blank=True, max_length=50, null=True)),
                ('talla', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Oficial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=11)),
                ('cargo', models.CharField(max_length=50)),
                ('ubicacion', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('instalado', 'Instalado'), ('disponible', 'Disponible'), ('ausente', 'Ausente'), ('licencia', 'Licencia'), ('transferido', 'Transferido')], max_length=50)),
                ('fecha_ingreso', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], max_length=10)),
                ('cantidad', models.PositiveIntegerField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('responsable', models.CharField(blank=True, max_length=100)),
                ('observaciones', models.TextField(blank=True)),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operaciones.articuloinventario')),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoArma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrega', 'Entrega'), ('devolucion', 'Devolución'), ('transferencia', 'Transferencia')], max_length=20)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('observaciones', models.TextField(blank=True)),
                ('arma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operaciones.arma')),
                ('oficial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='operaciones.oficial')),
            ],
        ),
        migrations.AddField(
            model_name='arma',
            name='asignada_a',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='operaciones.oficial'),
        ),
    ]
