from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('operaciones.urls')),  # 👈 agrega esta línea
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







from django.contrib import admin
from django.urls import path
from operaciones.views import portal_home, detalle_arma  # importa la vista aquí

urlpatterns = [
    path("admin/", admin.site.urls),
    path("portal/", portal_home, name="portal_home"),  # 👈 esta línea es clave
    path("arma/<int:arma_id>/", detalle_arma, name="detalle_arma"),
    path("login/", ...),
    path("logout/", ...),
]
