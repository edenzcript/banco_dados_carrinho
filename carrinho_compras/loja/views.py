from django.shortcuts import render
from django.http import HttpResponse
from .models import Produto

def home(request):
    return render(request, 'home.html')

def carrinho(request):
    carrinho = request.session.get('carrinho', [])

    itens = []
    total = 0
    for item in carrinho:
        try:
            produto = Produto.objects.get(id=item['produto_id'])

            item['produto'] = produto
            item['total'] = produto.preco * item['quantidade']
            itens.append(item)
            total += item['total']
        except Produto.DoesNotExist:
            continue

    # Passa os dados para o template para renderizar a página do carrinho
    return render(request, 'carrinho_compras.html', {
        'carrinho': carrinho,
        'itens': itens,
        'total': total,
    })


# Função para adicionar um item ao carrinho
def adicionar_ao_carrinho(request, produto_id):
    # Verifica se o carrinho já existe na sessão
    carrinho = request.session.get('carrinho', [])

    produto_existente = next((item for item in carrinho if item['produto_id'] == produto_id), None)

    if produto_existente:
        produto_existente['quantidade'] += 1
    else:
        carrinho.append({'produto_id': produto_id, 'quantidade': 1})
    request.session['carrinho'] = carrinho

    return HttpResponse("Produto adicionado ao carrinho.")


# Função para remover um item do carrinho
def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', [])
    carrinho = [item for item in carrinho if item['produto_id'] != produto_id]
    request.session['carrinho'] = carrinho

    return HttpResponse("Produto removido do carrinho.")


# Função para limpar o carrinho
def limpar_carrinho(request):
    request.session['carrinho'] = []
    return HttpResponse("Carrinho limpo.")