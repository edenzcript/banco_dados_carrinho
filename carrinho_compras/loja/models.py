from django.db import models
from django.contrib.auth.models import User


# Modelo de Pedido
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('processando', 'Processando'),
            ('enviado', 'Enviado'),
            ('entregue', 'Entregue'),
            ('cancelado', 'Cancelado'),
        ],
        default='pendente'
    )

    def __str__(self):
        return f'Pedido {self.id} de {self.usuario.username}'

    def total(self):
        return sum(item.total() for item in self.itens.all())

    class Meta:
        ordering = ['-data_pedido']


# Modelo de Cliente
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, unique=True)  # Tornando telefone único
    data_nascimento = models.DateField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


# Modelo de Categoria
class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)  # Garantir que o nome seja único

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


# Modelo de Produto com relação à Categoria
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)  # Relacionando a categoria

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.estoque < 0:
            raise ValueError("Estoque não pode ser negativo")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


# Modelo de Carrinho
class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Definindo o ID de um usuário padrão
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('aberto', 'Aberto'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado')],
        default='aberto'
        )
    def __str__(self):
        return f'Carrinho de {self.usuario.username}'

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'


# Modelo de ItemCarrinho
class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} no carrinho de {self.carrinho.usuario.username}'

    def total(self):
        return self.quantidade * self.produto.preco

    def save(self, *args, **kwargs):
        # Verificar se a quantidade solicitada não excede o estoque
        if self.quantidade > self.produto.estoque:
            raise ValueError("Quantidade em estoque insuficiente")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'


# Modelo de ItemPedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} no pedido {self.pedido.id}'

    def total(self):
        return self.quantidade * self.produto.preco

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
