# existing imports
from django.urls import path
from django.conf.urls import url
from apiAnalisis import views

urlpatterns = [
    path('libros/', views.ListLibro.as_view()),
    path('libros/<int:pk>/', views.DetailLibro.as_view()),
    path('clientes/', views.ListCliente.as_view()),
    path('clientes/<int:pk>/', views.DetailCliente.as_view()),
    path('clientesFiltroDinamico/', views.ClientesAPIView.as_view()),
    path('clientesporcedula/', views.CedulaClientesAPIView.as_view()),
    path('clientesportipo/', views.TipoClientesAPIView.as_view()),
    #path('clientes/<int:cedula>/', views.DetailCliente.as_view()),
    path('graficas/', views.ListGrafica.as_view()),
    path('graficas/<int:pk>/', views.DetailGrafica.as_view()),
    url(r'^mostrarInterfazPredecir/',views.Clasificacion.mostrarInterfazPredecir),
    url(r'^predecirTipoCliente/',views.Clasificacion.predecirTipoCliente),
    url(r'^$',views.Autenticacion.singIn),
    url(r'^postsign/',views.Autenticacion.postsign),
    path('mostrarInterfazBuscar/', views.Clasificacion.mostrarInterfazBuscar),
    path('buscarCliente/', views.Clasificacion.buscarCliente),
    url(r'^mostrarInterfazPredecirConEstilo/',views.Clasificacion.mostrarInterfazPredecirConEstilo),
    
]