from django.contrib import admin, messages
from django.db.models import QuerySet
from.import models
# Register your models here.
# admin.site.register(models.Produtos)
admin.site.register(models.Categorias)

@admin.register(models.Clientes)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'tipo_cliente']
    list_editable=[ 'nome', 'tipo_cliente']

class FiltroEstoque(admin.SimpleListFilter):
    title = 'Filtro Estoque'
    parameter_name = 'qtd'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Estoque Baixo'),
            ('0', 'Zerado'),
            ('>=10', 'OK')
        ]
       
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(
                qtd__lte=10,
                qtd__gte=1)
        if self.value() == '0':
            return queryset.filter(qtd=0)
        if self.value() == '>=10':
            return queryset.filter(qtd__gte=10)

@admin.register(models.Produtos)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'avaliar_estoque', 'qtd', 'categoria', 'validade', 'descricao', 'disponibilidade']
    list_editable=['qtd']
    actions=['zerar_estoque', 'aumentar_preco_30']
    search_fields = ['nome_istartswith']
    list_filter = [FiltroEstoque]

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

    
class Meta:
    verbose_name_plural = 'Admin'