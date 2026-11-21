from django.contrib import admin

# Register your models here.
from .models import Denuncia, Historico, Observacao

admin.site.register(Denuncia)
admin.site.register(Historico)
admin.site.register(Observacao)