from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator
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

class CategoriaEntrada(models.Model):
    nome = models.CharField(unique = True, max_length = 50)
    descricao = models.CharField(blank = True, null = True, max_length = 100)
    
    class Meta:
        db_table = 'categoria_entrada'
        verbose_name = 'categoria de entrada'
        verbose_name_plural = 'Categorias de Entrada'

    def __str__(self):
        return self.nome

class CategoriaSaida(models.Model):
    nome = models.CharField(unique = True, max_length = 30)
    descricao = models.CharField(blank = True, null = True, max_length = 100)

    class Meta:
        db_table = 'categoria_saida'
        verbose_name = 'categoria de saída'
        verbose_name_plural = 'Categorias de Saída'

    def __str__(self):
        return self.nome

class Congregacao(models.Model):
    nome = models.CharField(max_length = 70)
    localidade = models.CharField(max_length = 50)
    
    class Meta:
        db_table = 'congregacao'
        verbose_name = 'congregação'
        verbose_name_plural = 'congregações'

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

class Entrada(models.Model):
    membro = models.ForeignKey('Membro', on_delete = models.CASCADE)
    congregacao = models.ForeignKey('Congregacao', on_delete = models.CASCADE)
    data = models.DateField(default = date.today)
    valor = models.DecimalField(max_digits = 12, decimal_places = 2)
    forma_de_Pagamento = models.ForeignKey('Pagamento', on_delete = models.CASCADE)
    categoria = models.ForeignKey('CategoriaEntrada', on_delete = models.CASCADE)
    descricao = models.CharField(blank = True, null = True, max_length = 100)
    comprovante = models.FileField(blank = True, null = True, validators = [FileExtensionValidator(['jpeg', 'jpg', 'pdf', 'png'])], upload_to = 'documentos/comprovantes/entradas')
    administrador = models.ForeignKey('Administrador', on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'entrada'

    def __str__(self):
        return str(self.valor)

    def delete(self, *args, **kwargs):
        os.remove(self.comprovante.path)
        super(Entrada, self).delete(*args, **kwargs)

class EntradaAvulsa(models.Model):
    valor = models.DecimalField(max_digits = 12, decimal_places = 2)
    data = models.DateField(default = date.today)
    congregacao = models.ForeignKey('Congregacao', on_delete = models.CASCADE)
    descricao = models.CharField(blank = True, null = True, max_length = 100)
    comprovante = models.FileField(blank = True, null = True, validators = [FileExtensionValidator(['jpeg', 'jpg', 'pdf', 'png'])], upload_to = 'documentos/comprovantes/entrada_avulsa')
    administrador = models.ForeignKey('Administrador', on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'entrada_avulsa'
        verbose_name_plural = 'Entradas Avulsa'

    def __str__(self):
        return 'R$ ' + str(self.valor)
    
    def delete(self, *args, **kwargs):
        os.remove(self.comprovante.path)
        super(EntradaAvulsa, self).delete(*args, **kwargs)

class EntradaMissao(models.Model):
    valor = models.DecimalField(max_digits = 12, decimal_places = 2)
    missao = models.ForeignKey('Missao', on_delete = models.CASCADE)
    data = models.DateField(default = date.today)

    class Meta:
        db_table = 'entrada_missao'
        verbose_name = 'entrada de missão'
        verbose_name_plural = 'Entradas de Missões'

    def __str__(self):
        return 'R$ ' + str(self.valor)

class Membro(models.Model):
    CPF = models.CharField(unique = True, blank = True, null = True, max_length = 15, validators = [MinLengthValidator(11)])
    nome = models.CharField(max_length = 75)
    telefone = models.CharField(blank = True, null = True, max_length = 14, validators = [MinLengthValidator(8)])
    salario = models.DecimalField(blank = True, null = True, max_digits = 12, decimal_places = 2)

    class Meta:
        db_table = 'membro'

    def __str__(self):
        return self.nome

class Missao(models.Model):
    nome = models.CharField(max_length = 50)
    descricao = models.CharField(blank = True, null = True, max_length = 100)
    congregacao = models.ForeignKey('Congregacao', on_delete = models.CASCADE)
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

class Pagamento(models.Model):
    nome = models.CharField(unique = True, max_length = 50)
    descricao = models.CharField(blank = True, null = True, max_length = 100)
    
    class Meta:
        db_table = 'pagamento'

    def __str__(self):
        return self.nome

class Saida(models.Model):
    nome = models.CharField(max_length = 75)
    categoria = models.ForeignKey('CategoriaSaida', on_delete = models.CASCADE)
    descricao = models.CharField(blank = True, null = True, max_length = 100)
    empresa = models.ForeignKey('Empresa', on_delete = models.CASCADE)
    data = models.DateField(default = date.today)
    valor = models.DecimalField(max_digits = 12, decimal_places = 2)
    comprovante = models.FileField(blank = True, null = True, validators = [FileExtensionValidator(['jpeg', 'jpg', 'pdf', 'png'])], upload_to = 'documentos/comprovantes/saidas')
    nota_Fiscal = models.FileField(blank = True, null = True, validators = [FileExtensionValidator(['jpeg', 'jpg', 'pdf', 'png'])], upload_to = 'documentos/notas_fiscais')
    administrador = models.ForeignKey('Administrador', on_delete = models.CASCADE)
    postado = models.DateTimeField(default = datetime.today)

    class Meta:
        db_table = 'saida'
        verbose_name = 'saída'
        verbose_name_plural = 'saídas'

    def __str__(self):
        return self.nome

    def delete(self, *args, **kwargs):
        os.remove(self.comprovante.path)
        os.remove(self.nota_Fiscal.path)
        super(Saida, self).delete(*args, **kwargs)