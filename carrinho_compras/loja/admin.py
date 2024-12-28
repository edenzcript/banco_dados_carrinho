from django.contrib import admin
from .models import Produto, Carrinho, ItemCarrinho, Pedido, ItemPedido  # Verifique se 'Pedido' existe em models.py

admin.site.register(Produto)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
admin.site.register(Pedido)  
admin.site.register(ItemPedido)
