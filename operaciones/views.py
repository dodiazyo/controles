from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date, timedelta
from .models import Arma, DocumentoVehiculo
from .forms import ArmaForm


@login_required
def registrar_arma(request):
    if request.method == 'POST':
        form = ArmaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('portal_home')  # o redirige a un listado de armas si lo tienes
    else:
        form = ArmaForm()
    return render(request, 'operaciones/registro_arma.html', {'form': form})



@login_required
def licencias_vencidas(request):
    hoy = date.today()
    pronto = hoy + timedelta(days=30)

    armas_vencidas = Arma.objects.filter(fecha_vencimiento_licencia__lt=hoy)
    armas_por_vencer = Arma.objects.filter(fecha_vencimiento_licencia__range=(hoy, pronto))

    docs_vencidos = DocumentoVehiculo.objects.filter(fecha_vencimiento__lt=hoy)
    docs_por_vencer = DocumentoVehiculo.objects.filter(fecha_vencimiento__range=(hoy, pronto))

    return render(request, 'portal/licencias.html', {
        'armas_vencidas': armas_vencidas,
        'armas_por_vencer': armas_por_vencer,
        'docs_vencidos': docs_vencidos,
        'docs_por_vencer': docs_por_vencer
    })


@login_required
def portal_home(request):
    return render(request, 'portal/home.html')  # Tu portal principal


def detalle_arma(request, arma_id):
    arma = get_object_or_404(Arma, id=arma_id)
    return render(request, 'operaciones/detalle_arma.html', {'arma': arma})


@login_required
def lista_armas(request):
    armas = Arma.objects.all()
    return render(request, 'portal/armas/lista.html', {'armas': armas})
