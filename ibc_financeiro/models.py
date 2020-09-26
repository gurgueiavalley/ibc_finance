from django.db import models
from django.core.validators import MinLengthValidator
from datetime import date, datetime
import os

class Administrador(models.Model):
    nome = models.CharField(max_length = 70)
    username = models.CharField(unique = True, max_length = 30)
    email = models.EmailField(unique = True, max_length = 70)
    senha = models.CharField(max_length = 25, validators = [MinLengthValidator(5)])

    class Meta:
        db_table = 'administrador'
        verbose_name_plural = 'administradores'

    def __str__(self):
        return self.nome 

class Contador(models.Model):
    nome = models.CharField(max_length = 70)
    username = models.CharField(unique = True, max_length = 30)
    email = models.EmailField(unique = True, max_length = 70)
    senha = models.CharField(max_length = 25, validators = [MinLengthValidator(5)])

    class Meta:
        db_table = 'contador'
        verbose_name_plural = 'contadores'

    def __str__(self):
        return self.nome

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
        db_table = 'entrada_missao'
        verbose_name = 'entrada de missão'
        verbose_name_plural = 'Entradas de Missões'

    def __str__(self):
        return str(self.valor)

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

class Saida(models.Model):
    nome = models.CharField(max_length = 75)
    categoria = models.ForeignKey('SaidaCategoria', on_delete = models.CASCADE)
    descricao = models.CharField(blank = True, null = True, max_length = 100)
    empresa = models.ForeignKey('Empresa', on_delete = models.CASCADE)
    data = models.DateField(default = date.today)
    valor = models.DecimalField(max_digits = 12, decimal_places = 2)
    comprovante = models.FileField(blank = True, null = True, upload_to = 'documentos/comprovantes')
    nota_Fiscal = models.FileField(blank = True, null = True, upload_to = 'documentos/notas')
    administrador = models.ForeignKey('AdminCongregacao', on_delete = models.CASCADE)
    postado = models.DateTimeField(default = datetime.today)

    class Meta:
        db_table = 'saida'

    def __str__(self):
        return self.nome

    def delete(self, *args, **kwargs):
        os.remove(self.comprovante.path)
        os.remove(self.nota_Fiscal.path)
        super(Saida, self).delete(*args, **kwargs)

class SaidaCategoria(models.Model):
    nome = models.CharField(unique = True, max_length = 50)
    descricao = models.CharField(blank = True, null = True, max_length = 100)

    class Meta:
        db_table = 'saida_categoria'
        verbose_name = 'categoria de saída'
        verbose_name_plural = 'Categorias de Saída'

    def __str__(self):
        return self.nome


class Membro(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14, unique = True)
    salario = models.FloatField()
    telefone = models.CharField(max_length=13)

    def __str__(self):
        return self.nome

class CategoriaEntrada(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nome

class FormaPagamento(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nome

class Congregacao(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nome

class EntradaFinanceiraAvulca(models.Model):
    descricao = models.CharField(max_length=200)
    data = models.DateTimeField(auto_now=True)
    valor = models.FloatField()
    congregacao = models.OneToOneField(Congregacao, on_delete=models.CASCADE)
    admin_congregacao = models.ForeignKey(AdminCongregacao, on_delete=models.CASCADE)   
    
    def __str__(self):
        return self.descricao 

class EntradaFinanceira(models.Model):
    descricao = models.CharField(max_length=200)
    data = models.DateTimeField(auto_now=True)
    valor = models.FloatField()
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    congregacao = models.ForeignKey(Congregacao, on_delete=models.CASCADE)
    categoria_entrada = models.ForeignKey(CategoriaEntrada, on_delete=models.CASCADE)
    adm_congregacao = models.ForeignKey(AdminCongregacao, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.descricao
