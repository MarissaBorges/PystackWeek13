from django.shortcuts import render, redirect	
from django.http import HttpResponse, Http404
from . models import Mentorados, Navigators, DisponibilidadedeHorarios, Reuniao, Tarefa, Upload
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from . auth import valida_token
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def mentorados(request):

    # if not request.user.is_authenticated:
    #     return redirect('login')
    
    if request.method == 'GET':
        navigators = Navigators.objects.filter(user=request.user)
        mentorados = Mentorados.objects.filter(user=request.user)

        estagios_flat = []
        for i in Mentorados.estagio_choices:
            estagios_flat.append(i[1])

        qtd_estagios = []
        for i,j in Mentorados.estagio_choices:
            x = Mentorados.objects.filter(estagio=i).filter(user=request.user).count()
            qtd_estagios.append(x)

        return render(request, 'mentorados.html', {'estagios': Mentorados.estagio_choices, 'navigators': navigators, 'mentorados': mentorados, 'estagios_flat': estagios_flat, 'qtd_estagios': qtd_estagios})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')
        estagio = request.POST.get('estagio')
        navigator = request.POST.get('navigator')

        mentorado = Mentorados(
            nome= nome,
            foto=foto,
            estagio=estagio,
            navigator_id=navigator,
            user=request.user
        )

        mentorado.save()

        mentorado = Mentorados.objects.get(nome=nome)
        messages.add_message(request, constants.SUCCESS, f'Mentorado registrado com sucesso. Token de acesso: {mentorado.token}')
        return redirect('mentorados')

@login_required
def reunioes(request):

    if request.method == 'GET':
        reunioes = Reuniao.objects.filter(data__mentor=request.user)

        return render(request, 'reunioes.html', {'reunioes':reunioes})
    
    elif request.method == 'POST':
        data = request.POST.get('data')
        data = datetime.strptime(data, '%Y-%m-%dT%H:%M')

        disponibilidades = DisponibilidadedeHorarios.objects.filter(mentor = request.user).filter(
            data_inicial__gte=(data - timedelta(minutes=50)),
            data_inicial__lte=(data + timedelta(minutes=50))
        )

        if disponibilidades.exists():
            messages.add_message(request, constants.ERROR, 'Você ja possui uma reunião em aberto, cada reunião dura 50 minutos.')
            return redirect('reunioes')

        disponibilidades = DisponibilidadedeHorarios(
            data_inicial = data,
            mentor = request.user,

        )

        disponibilidades.save()

        messages.add_message(request, constants.SUCCESS, 'Horário disponibilizado com sucesso!!')
        return redirect('reunioes')
    
@csrf_protect
def auth(request):

    if request.method == 'GET':
        return render(request, 'auth_mentorado.html')
    elif request.method == 'POST':
        token = request.POST.get('token')

        if not Mentorados.objects.filter(token=token).exists():
            messages.add_message(request, constants.ERROR, 'Token de acesso inválido!!')
            return redirect('auth_mentorado')
        
    
        response = redirect('escolher_dia')
        response.set_cookie('auth_token', token, max_age=3600)

        return response
    
def escolher_dia(request):

    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')

    if request.method == 'GET':
        mentorado = valida_token(request.COOKIES.get('auth_token'))
        disponibilidades = DisponibilidadedeHorarios.objects.filter(
            data_inicial__gte = datetime.now(),
            agendado = False,
            mentor = mentorado.user
        ).values_list('data_inicial', flat= True)

        dias_semana_nomes = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
               'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

        datas_completas = []
        datas = []
        dias_semana = []
        meses = []

        datas_vistas = set()  # Para evitar duplicatas

        for data in disponibilidades:
            dia = data.date()
            data_formatada = dia.strftime('%d-%m-%Y')

            if data_formatada not in datas_vistas:
                datas_vistas.add(data_formatada)

                datas.append(data_formatada)
                dias_semana.append(dias_semana_nomes[dia.weekday()])
                meses.append(meses_nomes[dia.month - 1])

            datas_completas = list(zip(datas, dias_semana, meses))


        return render(request, 'escolher_dia.html', {'datas':datas_completas})
    
def agendar_reuniao(request):

    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')
    

    mentorado = valida_token(request.COOKIES.get('auth_token'))

    #TODO validar se os horarios disponiveis são realmente de um mentor

    if request.method == 'GET':
        data = request.GET.get('data')
        data = datetime.strptime(data, '%d-%m-%Y')
        
        horarios = DisponibilidadedeHorarios.objects.filter(
            data_inicial__gte = data,
            data_inicial__lt = data + timedelta(days=1),
            agendado = False,
            mentor = mentorado.user
        )

        return render(request, 'agendar_reuniao.html', {'horarios': horarios, 'tags': Reuniao.tag_choices})

    else:
        horario_id = request.POST.get('horario')
        tag = request.POST.get('tag')
        descricao = request.POST.get('descricao')

        # técnica para pesquisar: ATOMICIDADE
        reuniao = Reuniao(
            data_id = horario_id,
            mentorado = mentorado,
            tag = tag,
            descricao = descricao
        )
        reuniao.save()

        horario = DisponibilidadedeHorarios.objects.get(id = horario_id)
        horario.agendado = True
        horario.save()

        messages.add_message(request, constants.SUCCESS, 'Reunião agendada com sucesso.')
        return redirect('escolher_dia')

@login_required
def tarefa(request, id):
    mentorado = Mentorados.objects.get(id = id)
    if mentorado.user != request.user:
        raise Http404()
    
    if request.method == 'GET':
        tarefas = Tarefa.objects.filter(mentorado=mentorado)
        videos = Upload.objects.filter(mentorado=mentorado)
        return render(request, 'tarefa.html', {'mentorado': mentorado, 'tarefas':tarefas, 'videos':videos})

    else:
        tarefa = request.POST.get('tarefa')

        tarefa = Tarefa(
            mentorado = mentorado,
            tarefa = tarefa
        )
        tarefa.save()

        return redirect(f'/mentorados/tarefa/{id}')
    
@login_required
def upload(request, id):
    mentorado = Mentorados.objects.get(id = id)
    if mentorado.user != request.user:
        raise Http404()
    
    video = request.FILES.get('video')
    upload = Upload(
        mentorado = mentorado,
        video = video
    )

    upload.save()
    return redirect(f'/mentorados/tarefa/{id}')

def tarefa_mentorado(request):
    mentorado = valida_token(request.COOKIES.get('auth_token'))
    if not mentorado:
        return redirect('auth_mentorado')
    
    if request.method == 'GET':
        videos = Upload.objects.filter(mentorado=mentorado)
        tarefas = Tarefa.objects.filter(mentorado=mentorado)
        return render(request, 'tarefa_mentorado.html', {'mentorado': mentorado, 'videos': videos, 'tarefas': tarefas})
    
@csrf_exempt
def tarefa_alterar(request, id):
    mentorado = valida_token(request.COOKIES.get('auth_token'))
    if not mentorado:
        return redirect('auth_mentorado')

    tarefa = Tarefa.objects.get(id=id)
    if mentorado != tarefa.mentorado:
        raise Http404()
    tarefa.realizada = not tarefa.realizada
    tarefa.save()

    return HttpResponse('teste')
    