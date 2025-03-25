from django.contrib import admin
from .models import Flower, Event, Order, CustomUser, BouquetOfFlowers, Consultation


class EventAdminInline(admin.TabularInline):
    model = BouquetOfFlowers.events.through


class FlowerInline(admin.TabularInline):
    model = BouquetOfFlowers.flowers.through


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'telegram_username']
    search_fields = ['username', 'telegram_username']


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]


@admin.register(BouquetOfFlowers)
class BouquetOfFlowersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price',]
    search_fields = ['name']
    list_filter = ['price', 'name']
    inlines = [EventAdminInline, FlowerInline]


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created']
    search_fields = ['customer__username']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'address', 'BouquetOfFlowers', 'delivery', 'status', 'total_price_with_currency']
    list_filter = ['delivery', 'status', 'BouquetOfFlowers']
    search_fields = ['customer__username', 'address', 'BouquetOfFlowers__name']

    def total_price_with_currency(self, obj):
        return f"{obj.total_price} руб."
    total_price_with_currency.short_description = 'Общая стоимость'

