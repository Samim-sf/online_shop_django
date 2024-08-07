from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'
    LESS_THAN_10 = '<10'

    def lookups(self, request, model_admin):
        return [
            (self.LESS_THAN_10, 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_10:
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 20
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    actions = ['clear_inventory']
    exclude = ['promotions']
    autocomplete_fields = ['collection']
    search_fields = ['title']
    prepopulated_fields = {'slug': ['title']}  # Automatically populate the slug from title

    def collection_title(self, product):
        return product.collection.title

    #
    # def get_fields(self, request, obj=None):
    #     # Include all fields you want to display/edit
    #     fields = ['title', 'unit_price', 'description', 'inventory', 'collection']
    #     if obj:
    #         # Include 'slug' when editing an existing object
    #         fields += ['slug']
    #     return fields

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         # Ensure 'slug' is read-only when editing an existing object
    #         return self.readonly_fields
    #     return self.readonly_fields
    #
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated'
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'number_orders']
    list_editable = ['membership']
    list_per_page = 20
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='number_orders')
    def number_orders(self, customer):
        url = reverse('admin:store_order_changelist') + '?' + urlencode({
            'customer__id': customer.id
        })

        return format_html('<a href= "{}">{}</a>', url, customer.number_orders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            number_orders=Count('order')
        )


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    min_num = 1
    autocomplete_fields = ['product']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    readonly_fields = ['placed_at']
    inlines = [OrderItemInline]


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
