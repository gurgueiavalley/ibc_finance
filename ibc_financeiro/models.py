from django.db import models
from django.core.validators import MinLengthValidator
from datetime import date

class Empresa(models.Model):
    CNPJ = models.CharField(unique = True, max_length = 18, validators = [MinLengthValidator(14)])
    nome = models.CharField(max_length = 70)
    descricao = models.CharField(max_length = 100, blank = True, null = True)
    endereco = models.CharField(max_length = 80) 
    cidade = models.CharField(max_length = 60, default = 'Corrente')

    class Meta:
        db_table = 'empresa'

    def __str__(self):
        return self.nome

class EntradaMissao(models.Model):
    valor = models.DecimalField(max_digits = 12, decimal_places = 2)
    missao = models.ForeignKey('Missao', on_delete = models.CASCADE)
    data = models.DateField(default = date.today)

    class Meta:
        db_table = 'entradamissao'
        verbose_name = 'entrada de missão'
        verbose_name_plural = 'Entradas de Missões'

    def __str__(self):
        return self.valor

class Missao(models.Model):
    nome = models.CharField(unique = True, max_length = 50)
    descricao = models.CharField(blank = True, null = True, max_length = 100)
    inicio = models.DateField(default = date.today)
    fim = models.DateField()
    em_Andamento = models.BooleanField(default = True)
    meta = models.DecimalField(max_digits = 12, decimal_places = 2)

    class Meta:
        db_table = 'missao'
        verbose_name = 'missão'
        verbose_name_plural = 'missões'

    def __str__(self):
        return self.nome