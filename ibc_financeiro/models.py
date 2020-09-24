from django.db import models
from django.core.validators import MinLengthValidator

class Empresa(models.Model):
    CNPJ = models.CharField(unique = True, max_length = 18, validators = [MinLengthValidator(14)])
    nome = models.CharField(max_length = 70)
    endereco = models.CharField(max_length = 80) 
    cidade = models.CharField(max_length = 60, default = 'Corrente')
    descricao = models.CharField(max_length = 100, blank = True, null = True)

    class Meta:
        db_table = 'empresa'

    def __str__(self):
        return self.nome