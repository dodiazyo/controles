from django.shortcuts import render, get_object_or_404
from .models import Arma
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def portal_home(request):
    return render(request, 'portal/home.html')  # Tu portal principal


def detalle_arma(request, arma_id):
    arma = get_object_or_404(Arma, id=arma_id)
    return render(request, 'operaciones/detalle_arma.html', {'arma': arma})
