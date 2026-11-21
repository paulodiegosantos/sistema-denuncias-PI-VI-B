from django.db import models
import uuid
from .fields import EncryptedTextField

# Create your models here.
class Denuncia(models.Model):

    TIPOS = [
        ('vazamento', 'Vazamento de dados'),
        ('seguranca', 'Prática inadequada de segurança'),
        ('suspeita', 'Atividade suspeita'),
    ]

    STATUS = [
        ('recebida', 'Recebida'),
        ('analise', 'Em análise'),
        ('investigacao', 'Em investigação'),
        ('concluida', 'Concluída'),
        ('arquivada', 'Arquivada'),
    ]

    protocolo = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    tipo = models.CharField(max_length=20, choices=TIPOS)
    descricao = EncryptedTextField()

    anonima = models.BooleanField(default=True)

    nome = EncryptedTextField(max_length=150, blank=True)
    email = EncryptedTextField(blank=True)
    empresa = EncryptedTextField(max_length=150, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='recebida'
    )

    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.protocolo)


class Historico(models.Model):

    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='historicos'
    )

    usuario = EncryptedTextField(max_length=150)
    acao = EncryptedTextField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.acao


class Observacao(models.Model):

    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='observacoes'
    )

    administrador = EncryptedTextField(max_length=150)
    texto = EncryptedTextField()
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Observação - {self.denuncia.protocolo}'
