from django.contrib import admin, messages
from.import models

# Register your models here.
# admin.site.register(models.Produtos)
admin.site.register(models.Categorias)
@admin.register(models.Clientes)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'tipo_cliente']
    list_editable=[ 'nome', 'tipo_cliente']
    list_filter=['tipo_cliente']    

@admin.register(models.Produtos)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'qtd', 'categoria', 'validade', 'descricao', 'disponibilidade']
    list_editable=['qtd']
    actions=['zerar_estoque', 'aumentar_preco_30']
    search_fields = ['nome_istartswith']

    @admin.display(ordering='qtd')
    def avaliar_estoque(self,produto):
        if produto.qtd < 0:
            produto.qtd = 0
            produto.save()
        if produto.qtd == 0:
            return "Zerado"
        if produto.qtd < 10:
            return 'Estoque Baixo'
        if produto.qtd >=10:
            return 'Estoque OK'

    @admin.action(description="+30 %% no preço")
    def aumentar_preco_30(self, request, queryset):
        porcentual = 0.3
        total_produtos = len(queryset)
        for produto in queryset:
            preco_antigo = float(produto.preco)
            preco_novo = preco_antigo + preco_antigo * porcentual
            produto.preco = preco_novo
            produto.save()
    
  
    @admin.action(description="Zerar Estoque")
    def zerar_estoque(self, request, queryset):
        total_atualizado = queryset.update(qtd=0)
        self.message_user(
            request,f'{total_atualizado}produtos foram atualizados',
            messages.WARNING
        )