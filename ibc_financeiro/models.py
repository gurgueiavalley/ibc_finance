from django.db import models

# Create your models here.
#Teste
class Membro(models.Model):
    nome = models.CharField(max_length=50)