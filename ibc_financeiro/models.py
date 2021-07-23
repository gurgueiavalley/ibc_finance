from django.db              import models
from django.core.validators import MinLengthValidator

from django.core.validators import FileExtensionValidator       # Validação de extensão de arquivo | validação de tamanho mínimo de caracteres
from django.contrib.auth.models import User                                         # Classe User padrão do Django
import os                                                                           # Manipulações de arquivos

class Categoria(models.Model):              # Categoria
    TIPOS = (       # Opções de tipo
        ('ENTRADA', 'ENTRADA'),     # Entrada
        ('SAÍDA', 'SAÍDA')          # Saída
    )

    nome = models.CharField(max_length = 35, unique = True)                                             # Nome (máximo de 35 caracteres | único | obrigatório)
    tipo = models.CharField(max_length = 7, validators = [MinLengthValidator(5)], choices = TIPOS)      # Tipo (máximo de 7 caracteres | mínimo de 5 caracteres | escolhas estáticas | obrigatório)
    
    def __str__(self):      # Nome do objeto
        return self.nome    # Retorna o nome da categoria

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()

        super(Categoria, self).save(*args, **kwargs)

class Congregacao(models.Model):            # Congregação
    nome = models.CharField(max_length = 60, unique = True)         # Nome (máximo de 60 caracteres | único | obrigatório)
    
    class Meta:             # Valores de leitura
        verbose_name = 'congregação'                # Nome da classe no singular
        verbose_name_plural = 'congregações'        # Nome da classe no plural

    def __str__(self):      # Nome do objeto
        return self.nome    # Retorna o nome

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()

        super(Congregacao, self).save(*args, **kwargs)

class Entrada(models.Model):                # Entrada
    membro = models.ForeignKey('Membro', on_delete = models.PROTECT)                                                                                                                            # Membro que ofertou (relacionamento [1,n] | protegida de deleção | obrigatório)
    valor = models.DecimalField(max_digits = 11, decimal_places = 2)                                                                                                                            # Valor ofertado (centena de milhões | duas casas decimais | obrigatório)
    transacao = models.ForeignKey('Transacao', on_delete = models.PROTECT)                                                                                                                      # Transação realizada para ofertar (relacionamento [1,n] | protegida de deleção | obrigatório)
    data = models.DateField()                                                                                                                                                                   # Data ofertada (obrigatório)
    comprovante = models.FileField(upload_to = 'financeiro/entradas/comprovantes/membros', blank = True, null = True, validators = [FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])])     # Comprovante da oferta (diretório de armazenagem | opcional | extensões permitidas)
    categoria = models.ForeignKey(Categoria, on_delete = models.PROTECT)                                                                                                                        # Categoria que foi destinada (relacionamento [1,n] | protegida de deleção | obrigatório)
    congregacao = models.ForeignKey(Congregacao, on_delete = models.PROTECT)                                                                                                                    # Congregação que recebeu (relacionamento [1,n] | protegida de deleção | obrigatório)
    anotacao = models.CharField(max_length = 50, blank = True, null = True)                                                                                                                     # Anotação adicional (máximo de 50 caracteres | opcional)
    usuario = models.ForeignKey(User, on_delete = models.PROTECT)                                                                                                                               # Usuário que cadastrou (relacionamento [1,n] | protegida de deleção | obrigatório)

    def __str__(self):                      # Nome do objeto
        return 'R$ ' + str(self.valor)      # Retorna o símbolo do real com o valor

    def save(self, *args, **kwargs):        # Deletar os arquivos na alteração
        try:        # Faz o teste
            salvo = Entrada.objects.get(id = self.id)       # Pega os dados salvos no banco

            if salvo.comprovante != self.comprovante:       # Se o comprovante salvo não for igual o atual
                os.remove(salvo.comprovante.path)           # Deleta o comprovante salvo

        except:     # Caso de erro no teste
            pass    # Não faz nada

        if self.anotacao:
            self.anotacao = self.anotacao.upper()

        super(Entrada, self).save(*args, **kwargs)      # Continua a alteração no banco de dados

    def delete(self, *args, **kwargs):      # Deletar os arquivos na deleção
        if bool(self.comprovante):                      # Se tiver comprovante salvo
            os.remove(self.comprovante.path)            # Deleta o arquivo
        
        super(Entrada, self).delete(*args, **kwargs)    # Continua a deleção das informações do banco de dados

class EntradaAvulsa(models.Model):          # Entrada Avulsa
    valor = models.DecimalField(max_digits = 11, decimal_places = 2)                                                                                                                            # Valor ofertado (centena de milhões | duas casas decimais | obrigatório)
    transacao = models.ForeignKey('Transacao', on_delete = models.PROTECT)                                                                                                                      # Transação realizada para ofertar (relacionamento [1,n] | protegida de deleção | obrigatório)
    data = models.DateField()                                                                                                                                                                   # Data que foi feito a oferta (obrigatório)
    comprovante = models.FileField(upload_to = 'financeiro/entradas/comprovantes/avulsas', blank = True, null = True, validators = [FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])])     # Comprovante da oferta (diretório de armazenamento | opcional | extensões permitidas)
    congregacao = models.ForeignKey(Congregacao, on_delete = models.PROTECT)                                                                                                                    # Congregação que recebeu (relacionamento [1,n] | protegida de deleção | obrigatório)
    anotacao = models.CharField(max_length = 50, blank = True, null = True)                                                                                                                     # Anotação adicional (máximo de 50 caracteres | opcional)
    usuario = models.ForeignKey(User, on_delete = models.PROTECT)                                                                                                                               # Usuário que cadastrou (relacionamento [1,n] | protegida de deleção | obrigatório)
    
    class Meta:             # Valores de leitura
        verbose_name_plural = 'entradas avulsa'     # Nome da classe no plural

    def __str__(self):      # Nome do objeto
        return 'R$ ' + str(self.valor)      # Retorna o símbolo do real com o valor

    def save(self, *args, **kwargs):        # Deletar os arquivos na alteração
        try:        # Faz o teste
            salvo = EntradaAvulsa.objects.get(id = self.id)       # Pega os dados salvos no banco

            if salvo.comprovante != self.comprovante:       # Se o comprovante salvo não for igual o atual
                os.remove(salvo.comprovante.path)           # Deleta o comprovante salvo

        except:     # Caso de erro no teste
            pass    # Não faz nada

        if self.anotacao:
            self.anotacao = self.anotacao.upper()

        super(EntradaAvulsa, self).save(*args, **kwargs)      # Continua a alteração no banco de dados

    def delete(self, *args, **kwargs):      # Deletar os arquivos na deleção
        if bool(self.comprovante):              # Se tiver comprovante salvo
            os.remove(self.comprovante.path)    # Deleta o arquivo
        
        super(EntradaAvulsa, self).delete(*args, **kwargs)      # Continua a deleção das informações do banco de dados

class EntradaMissao(models.Model):          # Entrada de Missão
    valor = models.DecimalField(max_digits = 11, decimal_places = 2)                                                                                                                            # Valor ofertado (centena de milhões | duas casas decimais | obrigatório)
    transacao = models.ForeignKey('Transacao', on_delete = models.PROTECT)                                                                                                                      # Transação realizada para ofertar (relacionamento [1,n] | protegida de deleção | obrigatório)
    data = models.DateField()                                                                                                                                                                   # Data que foi feito a oferta (obrigatório)
    comprovante = models.FileField(upload_to = 'financeiro/entradas/comprovantes/missoes', blank = True, null = True, validators = [FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])])     # Comprovante da oferta (diretório de armazenamento | opcional | extensões permitidas)
    missao = models.ForeignKey('Missao', on_delete = models.PROTECT)                                                                                                                            # Missão que foi destinado a oferta (relacionamento [1,n] | protegida de deleção | obrigatório)
    anotacao = models.CharField(max_length = 50, blank = True, null = True)                                                                                                                     # Anotação adicional (máximo de 50 caracteres | opcional)
    usuario = models.ForeignKey(User, on_delete = models.PROTECT)                                                                                                                               # Usuário que cadastrou (relacionamento [1,n] | protegida de deleção | obrigatório)

    class Meta:                             # Valores de leitura
        verbose_name = 'entrada de missão'                  # Nome da classe no singular
        verbose_name_plural = 'entradas de missões'         # Nome da classe no plural

    def __str__(self):                      # Nome do objeto
        return 'R$ ' + str(self.valor)      # Retorna o símbolo do real com o valor

    def save(self, *args, **kwargs):        # Deletar os arquivos na alteração
        try:        # Faz o teste
            salvo = EntradaMissao.objects.get(id = self.id)       # Pega os dados salvos no banco

            if salvo.comprovante != self.comprovante:       # Se o comprovante salvo não for igual o atual
                os.remove(salvo.comprovante.path)           # Deleta o comprovante salvo

        except:     # Caso de erro no teste
            pass    # Não faz nada

        if self.anotacao:
            self.anotacao = self.anotacao.upper()

        super(EntradaMissao, self).save(*args, **kwargs)      # Continua a alteração no banco de dados

    def delete(self, *args, **kwargs):      # Deletar os arquivos na deleção
        if bool(self.comprovante):              # Se tiver comprovante salvo
            os.remove(self.comprovante.path)    # Deleta o arquivo
        
        super(EntradaMissao, self).delete(*args, **kwargs)      # Continua a deleção das informações do banco de dados

class Fornecedor(models.Model):             # Fornecedor
    documento = models.CharField(max_length = 15, unique = True, validators = [MinLengthValidator(14)])     # CPF ou CNPJ (máximo de 15 caracteres | único | mínimo de 14 caracteres | obrigatório)
    nome = models.CharField(max_length = 70)                                                                # Nome (máximo de 70 caracteres | obrigatório)
    descricao = models.CharField(max_length = 50, blank = True, null = True)                                # Descrição dos tipos de produtos/serviços (máximo de 50 caracteres | opcional)
    endereco = models.CharField(max_length = 100, blank = True, null = True)                                # Endereço completo (máximo de 100 caracteres | opcional)

    class Meta:             # Valores de leitura
        verbose_name_plural = 'fornecedores'    # Nome da classe no plural

    def __str__(self):      # Nome do objeto
        return self.nome    # Retorna o nome

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()

        if self.descricao:
            self.descricao = self.descricao.upper()

        if self.endereco:
            self.endereco = self.endereco.upper()

        super(Fornecedor, self).save(*args, **kwargs)

class Membro(models.Model):
    SEXES = (('Masculino', 'Masculino'), ('Feminino', 'Feminino'))

    CPF = models.CharField(blank = True, null = True, validators = [MinLengthValidator(14)], max_length = 14, unique = True)
    nome = models.CharField(max_length = 50)
    sex = models.CharField(blank = True, null = True, choices = SEXES, validators = [MinLengthValidator(8)], max_length = 9)
    birth = models.DateField(blank = True, null = True)
    cell = models.CharField(blank = True, null = True, validators = [MinLengthValidator(14)], max_length = 14, unique = True)
    email = models.EmailField(blank = True, null = True, max_length = 50, unique = True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.nome = self.nome.title()
        if self.email: self.email = self.email.lower()

        super(Membro, self).save(*args, **kwargs)

class Missao(models.Model):                 # Missão
    nome = models.CharField(max_length = 35)                                    # Nome (máximo de 35 caracteres | obrigatório)
    detalhe = models.CharField(max_length = 45, blank = True, null = True)      # Detalhe do objetivo (máximo de 45 caracteres | opcional)
    meta = models.DecimalField(max_digits = 11, decimal_places = 2)             # Meta de quanto pretende receber (centena de milhões | duas casas decimais | obrigatório)
    congregacao = models.ForeignKey(Congregacao, on_delete = models.PROTECT)    # Congregação que realizou (relacionamento [1,n] | protegida de deleção | obrigatório)
    inicio = models.DateField()                                                 # Data que iniciou ou vai iniciar (obrigatório)
    fim = models.DateField()                                                    # Data que finalizou ou vai finalizar (obrigatório)
    andamento = models.BooleanField()                                           # Está em andamento (obrigatório)

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()

        if self.detalhe:
            self.detalhe = self.detalhe.upper()

        super(Missao, self).save(*args, **kwargs)

    class Meta:             # Valores de leitura
        verbose_name = 'missão'             # Nome da classe no singular
        verbose_name_plural = 'missões'     # Nome da classe no plural

    def __str__(self):      # Nome do objeto
        return self.nome    # Retorna o nome

class Saida(models.Model):                  # Saída
    congregacao = models.ForeignKey(Congregacao, on_delete = models.PROTECT)                                                                                                            # Congregação que fez o gasto (relacionamento [1,n] | protegida de deleção | obrigatório)
    nome = models.CharField(max_length = 35)                                                                                                                                            # Nome do produto ou serviço (máximo de 35 caracteres | obrigatório)
    descricao = models.CharField(max_length = 40, blank = True, null = True)                                                                                                            # Descrição do produto ou serviço (máximo de 40 caracteres | opcional)
    valor = models.DecimalField(max_digits = 11, decimal_places = 2)                                                                                                                    # Valor gasto (centena de milhoes | duas casas decimais | obrigatório)
    transacao = models.ForeignKey('Transacao', on_delete = models.PROTECT)                                                                                                              # Transação realizada para pagar (relacionamento [1,n] | protegida de deleção | obrigatório)
    data = models.DateField()                                                                                                                                                           # Data que foi gasto (obrigatório)
    comprovante = models.FileField(upload_to = 'financeiro/saidas/comprovantes', blank = True, null = True, validators = [FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])])       # Comprovante da compra (diretório de armazenagem | opcional | extensões permitidas)
    nf = models.FileField(upload_to = 'financeiro/saidas/nf', blank = True, null = True, validators = [FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])])                          # Comprovante do pagamento (diretório de armazenagem | opcional | extensões permitidas)
    categoria = models.ForeignKey(Categoria, on_delete = models.PROTECT)                                                                                                                # Categoria que o gasto se encaixa (relacionamento [1,n] | protegida de deleção | obrigatório)
    fornecedor = models.ForeignKey(Fornecedor, on_delete = models.PROTECT)                                                                                                              # Fornecedor do produto ou serviço (relacionamento [1,n] | protegida de deleção | obrigatório)
    usuario = models.ForeignKey(User, on_delete = models.PROTECT)                                                                                                                       # Usuário que cadastrou (relacionamento [1,n] | protegida de deleção | obrigatório)

    class Meta:                             # Valores de leitura
        verbose_name = 'saída'              # Nome da classe no singular
        verbose_name_plural = 'saídas'      # Nome da classe no plural

    def __str__(self):                      # Nome do objeto
        return self.nome    # Retorna o nome do produto ou serviço

    def save(self, *args, **kwargs):        # Deletar os arquivos na alteração
        try:        # Faz o teste
            salvo = Saida.objects.get(id = self.id)       # Pega os dados salvos no banco

            if salvo.comprovante != self.comprovante:       # Se o comprovante salvo não for igual o atual
                os.remove(salvo.comprovante.path)           # Deleta o comprovante salvo

            if salvo.nf != self.nf:             # Se a nota fiscal salva não for igual o atual
                os.remove(salvo.nf.path)        # Deleta a nota fiscal salva

        except:     # Caso de erro no teste
            pass    # Não faz nada

        self.nome = self.nome.upper()

        if self.descricao:
            self.descricao = self.descricao.upper()

        super(Saida, self).save(*args, **kwargs)      # Continua a alteração no banco de dados

    def delete(self, *args, **kwargs):      # Deletar os arquivos na deleção
        if bool(self.comprovante):              # Se tiver comprovante salvo
            os.remove(self.comprovante.path)    # Deleta o arquivo
        
        if bool(self.nf):               # Se tiver nota fiscal salva
            os.remove(self.nf.path)     # Deleta o arquivo 
        
        super(Saida, self).delete(*args, **kwargs)      # Continua o processo de deleção dos dados do banco

class Transacao(models.Model):              # Transação
    nome = models.CharField(max_length = 25, unique = True)     # Nome (máximo de 25 caracteres | único | obrigatório)
    
    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()

        super(Transacao, self).save(*args, **kwargs)

    class Meta:             # Valores de leitura
        verbose_name = 'transação'              # Nome da classe no singular
        verbose_name_plural = 'transações'      # Nome da classe no plural

    def __str__(self):      # Nome do objeto
        return self.nome    # Retorna o nome