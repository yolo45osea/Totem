from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name="index"),
    path('crear_reserva', views.crear_reserva, name="crear_reserva"),
    path('a', views.a, name="a"),
    path('reserva', views.reserva, name="reserva"),
    path('datos/<int:id_chofer>/<int:cupos>/<int:zona>/<str:horario>/', views.datos, name='datos'),
    path('pago/<int:chofer>/<int:cupos>/<str:nombre>/<str:email>/<str:rut>/<int:zona>/<str:horario>/<str:nombre1>/<str:email1>/<str:rut1>/<str:nombre2>/<str:email2>/<str:rut2>/<str:nombre3>/<str:email3>/<str:rut3>/', views.pago, name="pago"),
    path('codigoqr/<int:chofer>/<int:cupos>/<str:nombre>/<int:zona>/<str:horario>/<str:nombre1>/<str:nombre2>/<str:nombre3>/', views.codigoqr, name="codigoqr"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('inicio_admin', views.admin, name="inicio_admin"),
    path('adminSistema', views.adminSistema, name="adminSistema"),
    path('adminAeropuerto', views.adminAeropuerto, name="adminAeropuerto"),
    path('adminTransfer', views.adminTransfer, name="adminTransfer"),
    path('gestionUsuarios', views.gestionUsuarios, name="gestionUsuarios"),
    path('monitoreo', views.monitoreo, name="monitoreo"),
    path('gestionarTotem', views.gestionarTotem, name="gestionarTotem"),
    path('monitorearReservas', views.monitorearReservas, name="monitorearReservas"),
    path('GestionChoferes', views.GestionChoferes, name="GestionChoferes"),
    path('gestionZonas', views.gestionZonas, name="gestionZonas"),
]

