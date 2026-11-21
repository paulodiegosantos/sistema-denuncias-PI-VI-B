from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404

from .forms import DenunciaForm
from .models import Denuncia, Historico, Observacao

# Create your views here.
def staff_required(view_func):
    return user_passes_test(
        lambda user: (
            user.is_authenticated
            and user.is_active
            and user.is_staff
        ),
        login_url='login_admin'
    )(view_func)


def inicio(request):
    return render(request, 'denuncie/inicio.html')


def registrar_denuncia(request):
    if request.method == 'POST':
        form = DenunciaForm(request.POST)

        if form.is_valid():
            denuncia = form.save()

            Historico.objects.create(
                denuncia=denuncia,
                usuario='Sistema',
                acao='Denúncia registrada.'
            )

            return redirect(
                'confirmacao',
                protocolo=denuncia.protocolo
            )

    else:
        form = DenunciaForm()

    return render(
        request,
        'denuncie/registrar.html',
        {'form': form}
    )


def confirmacao(request, protocolo):
    try:
        denuncia = Denuncia.objects.get(protocolo=protocolo)
    except (
        Denuncia.DoesNotExist,
        ValueError,
        ValidationError
    ):
        raise Http404

    return render(
        request,
        'denuncie/confirmacao.html',
        {'denuncia': denuncia}
    )


def acompanhar_denuncia(request):
    denuncia = None
    erro = None

    if request.method == 'POST':
        protocolo = request.POST.get('protocolo', '').strip()

        try:
            denuncia = Denuncia.objects.get(protocolo=protocolo)

        except (
            Denuncia.DoesNotExist,
            ValueError,
            ValidationError
        ):
            erro = 'Protocolo não encontrado. Verifique o código informado.'

    return render(
        request,
        'denuncie/acompanhar.html',
        {
            'denuncia': denuncia,
            'erro': erro
        }
    )


@staff_required
def painel_admin(request):
    denuncias = Denuncia.objects.all().order_by('-criada_em')

    contexto = {
        'denuncias': denuncias,
        'total': denuncias.count(),
        'recebidas': denuncias.filter(status='recebida').count(),
        'analise': denuncias.filter(status='analise').count(),
        'investigacao': denuncias.filter(status='investigacao').count(),
    }

    return render(
        request,
        'denuncie/painel.html',
        contexto
    )


def login_admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('painel_admin')

    erro = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if (
            usuario is not None
            and usuario.is_staff
            and usuario.is_active
        ):
            login(request, usuario)
            return redirect('painel_admin')

        erro = 'Usuário ou senha inválidos.'

    return render(
        request,
        'denuncie/login.html',
        {'erro': erro}
    )


def logout_admin(request):
    if request.method == 'POST':
        logout(request)

    return redirect('login_admin')


@staff_required
def detalhe_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)

    if request.method == 'POST':
        novo_status = request.POST.get('status')
        status_validos = dict(Denuncia.STATUS)

        if novo_status not in status_validos:
            messages.error(request, 'Status inválido.')
            return redirect('detalhe_denuncia', pk=pk)

        status_anterior = denuncia.status

        observacao = request.POST.get(
            'observacao', ''
        ).strip()

        with transaction.atomic():

            if novo_status != status_anterior:
                denuncia.status = novo_status
                denuncia.save()

                Historico.objects.create(
                    denuncia=denuncia,
                    usuario=request.user.username,
                    acao=(
                        f'Status alterado de '
                        f'{status_anterior} para {novo_status}.'
                    )
                )

            if observacao:
                Observacao.objects.create(
                    denuncia=denuncia,
                    administrador=request.user.username,
                    texto=observacao
                )

                Historico.objects.create(
                    denuncia=denuncia,
                    usuario=request.user.username,
                    acao='Nova observação registrada.'
                )

        messages.success(
            request,
            'Denúncia atualizada com sucesso!'
        )

        return redirect('detalhe_denuncia', pk=pk)

    return render(
        request,
        'denuncie/detalhe.html',
        {'denuncia': denuncia}
    )
