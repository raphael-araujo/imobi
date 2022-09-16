from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cidade, Imovel, Visitas

# Create your views here.


@login_required(login_url='/auth/logar')
def home(request):
    cidades = Cidade.objects.all()
    preco_minimo = request.GET.get('preco_minimo')
    preco_maximo = request.GET.get('preco_maximo')
    cidade = request.GET.get('cidade')
    tipo = request.GET.getlist('tipo')
    if preco_minimo or preco_maximo or cidade or tipo:
        if not preco_minimo:
            preco_minimo = 0
        if not preco_maximo:
            preco_maximo = 9999999999
        if not tipo:
            tipo = ['A', 'C']

        imoveis = Imovel.objects.filter(valor__gte=preco_minimo) \
            .filter(valor__lte=preco_maximo) \
            .filter(tipo_imovel__in=tipo).filter(cidade=cidade)
    else:
        imoveis = Imovel.objects.all()

    return render(request, 'home.html', {'imoveis': imoveis, 'cidades': cidades})


@login_required(login_url='/auth/logar')
def imovel(request, id):
    imovel = get_object_or_404(Imovel, id=id)
    sugestoes = Imovel.objects.filter(cidade=imovel.cidade).exclude(id=id)[:3]

    return render(request, 'imovel.html', {'imovel': imovel, 'sugestoes': sugestoes})


@login_required(login_url='/auth/logar')
def agendar_visita(request):
    usuario = request.user
    dia = request.POST.get('dia')
    horario = request.POST.get('horario')
    id_imovel = request.POST.get('id_imovel')

    visitas = Visitas(
        imovel_id=id_imovel,
        usuario=usuario,
        dia=dia,
        horario=horario
    )
    visitas.save()

    return redirect('/agendamentos')


@login_required(login_url='/auth/logar')
def agendamentos(request):
    visitas = Visitas.objects.filter(usuario=request.user)
    return render(request, 'agendamentos.html', {'visitas': visitas})


@login_required(login_url='/auth/logar')
def cancelar_agendamento(request, id):
    visitas = get_object_or_404(Visitas, id=id)
    visitas.status = 'C'
    visitas.save()
    return redirect('/agendamentos')
