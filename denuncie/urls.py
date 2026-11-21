from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('denunciar/', views.registrar_denuncia, name='registrar'),
    path('confirmacao/<uuid:protocolo>/', views.confirmacao, name='confirmacao'),
    path('acompanhar/', views.acompanhar_denuncia, name='acompanhar'),
    path('administracao/login/', views.login_admin, name='login_admin'),
    path('administracao/', views.painel_admin, name='painel_admin'),
    path('administracao/sair/', views.logout_admin, name='logout_admin'),
    path('administracao/denuncia/<int:pk>/', views.detalhe_denuncia, name='detalhe_denuncia'),
]
