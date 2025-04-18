# Generated by Django 5.2 on 2025-04-18 17:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operaciones', '0006_licenciaconducir_vehiculo_mantenimientovehiculo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mantenimientovehiculo',
            old_name='fecha',
            new_name='fecha_mantenimiento',
        ),
        migrations.RenameField(
            model_name='vehiculo',
            old_name='año',
            new_name='anio',
        ),
        migrations.RenameField(
            model_name='vehiculo',
            old_name='zona',
            new_name='departamento',
        ),
        migrations.RemoveField(
            model_name='mantenimientovehiculo',
            name='archivo_factura',
        ),
        migrations.RemoveField(
            model_name='mantenimientovehiculo',
            name='detalle',
        ),
        migrations.RemoveField(
            model_name='mantenimientovehiculo',
            name='tipo',
        ),
        migrations.RemoveField(
            model_name='vehiculo',
            name='placa_documento',
        ),
        migrations.RemoveField(
            model_name='vehiculo',
            name='seguro_documento',
        ),
        migrations.RemoveField(
            model_name='vehiculo',
            name='supervisor_asignado',
        ),
        migrations.RemoveField(
            model_name='vehiculo',
            name='vencimiento_placa',
        ),
        migrations.RemoveField(
            model_name='vehiculo',
            name='vencimiento_seguro',
        ),
        migrations.AddField(
            model_name='mantenimientovehiculo',
            name='observaciones',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='mantenimientovehiculo',
            name='tipo_mantenimiento',
            field=models.CharField(default='General', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='kilometraje',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chequeodiario',
            name='imagen_1',
            field=models.ImageField(blank=True, null=True, upload_to='chequeos/'),
        ),
        migrations.AlterField(
            model_name='chequeodiario',
            name='imagen_2',
            field=models.ImageField(blank=True, null=True, upload_to='chequeos/'),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='placa',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='tipo',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='AsignacionVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona', models.CharField(max_length=50)),
                ('fecha_asignacion', models.DateField(auto_now_add=True)),
                ('licencia_supervisor', models.FileField(blank=True, null=True, upload_to='licencias_supervisores/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg'])])),
                ('fecha_vencimiento_licencia', models.DateField(blank=True, null=True)),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='operaciones.oficial')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operaciones.vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentoVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('placa', 'Placa'), ('seguro', 'Seguro')], max_length=20)),
                ('archivo', models.FileField(upload_to='documentos_vehiculo/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('fecha_vencimiento', models.DateField()),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operaciones.vehiculo')),
            ],
        ),
        migrations.DeleteModel(
            name='LicenciaConducir',
        ),
    ]
