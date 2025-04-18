from django.urls import path
from . import views

urlpatterns = [
    path('arma/<int:arma_id>/', views.detalle_arma, name='detalle_arma'),
]
