from django.urls import path
from .views import portal_home, detalle_arma
from .views import licencias_vencidas
from . import views



urlpatterns = [
    path("portal/", portal_home, name="portal_home"),  # 👈 ESTA ES LA QUE FALTA
    path("arma/<int:arma_id>/", detalle_arma, name="detalle_arma"),
    path('licencias/', licencias_vencidas, name='licencias'),
    path('portal/', views.portal_home, name='portal_home'),
    path('armas/', views.lista_armas, name='lista_armas'),
    path('armas/registrar/', views.registrar_arma, name='registrar_arma'),


]
