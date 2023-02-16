from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Categorias(models.Model):
    tipo = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.tipo

class Produtos(models.Model):
    nome = models.CharField(max_length=255)
    qtd = models.IntegerField(validators=[MinValueValidator(0, message="A quantidade deve ser maior ou igual a 0")])
    preco = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1, message="O preço deve ser igual ou maior que 1 real"), MaxValueValidator(1000)])
    categoria = models.CharField(max_length=50)
    descricao = models.TextField()
    validade = models.DateField()
    disponibilidade = models.BooleanField()

    categoria = models.ForeignKey(Categorias, on_delete = models.CASCADE)


    def __str__(self) -> str:
        return self.nome

class Clientes(models.Model):
    CLIENTE_FREE = 'F'
    CLIENTE_PREMIUM = 'P'
    CLIENTE_MASTER = 'M'

    TIPOS_CLIENTES = [
        (CLIENTE_FREE,'Free'),
        ('P','Premium'),
        ('M','Master'),
    ]
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=14)
    cpf = models.CharField(max_length=14)
    data_nascimento = models.DateField()
    data_cadastro = models.DateField(auto_now=True)
    tipo_cliente = models.CharField(max_length=1, choices=TIPOS_CLIENTES, default=CLIENTE_FREE)


class Meta:
    verbose_name_plural = 'Clientes'