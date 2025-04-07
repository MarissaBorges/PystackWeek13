from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import secrets

# Create your models here.
class Navigators(models.Model):
    nome = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # mentor 


    def __str__(self):
        return self.nome

class Mentorados(models.Model):
    estagio_choices = (('E1', '10-100k'), ('E2', '100-500k'), ('E3', '500-1000k'))
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    estagio =  models.CharField(max_length=2, choices=estagio_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # mentor
    navigator = models.ForeignKey(Navigators, null=True, blank=True, on_delete=models.CASCADE)
    criado_em = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=16)

    

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.gerar_token_unico()
        super().save(*args, **kwargs)

    def gerar_token_unico(self):
        while True:
            token = secrets.token_urlsafe(8)
            if not Mentorados.objects.filter(token=token).exists():
                return token
            


    def __str__(self):
        return self.nome
    
class DisponibilidadedeHorarios(models.Model):
    data_inicial = models.DateTimeField(null=True, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    agendado = models.BooleanField(default=False)

    def data_final(self):
        return self.data_inicial + timedelta(minutes=50)
    
class Reuniao(models.Model):

    tag_choices = (
        ('G', 'Gestão'),
        ('M', 'Marketing'),
        ('RH', 'Gestão de pessoas'),
        ('I', 'Impostos')
    )

    data = models.ForeignKey(DisponibilidadedeHorarios, on_delete=models.CASCADE)
    mentorado = models.ForeignKey(Mentorados, on_delete=models.CASCADE)
    tag = models.CharField(max_length=2, choices=tag_choices)
    descricao = models.TextField()

class Tarefa(models.Model):
    mentorado = models.ForeignKey(Mentorados, on_delete=models.CASCADE)
    tarefa = models.CharField(max_length=100)
    realizada = models.BooleanField(default=False)

class Upload(models.Model):
    mentorado = models.ForeignKey(Mentorados, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video')