from django.contrib import admin
from django.utils.html import format_html
from .models import Variable


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_display', 'value_display', 'type_badge', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'value']
    ordering = ['-created_at']
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información de la Variable', {
            'fields': ('name', 'value')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    @admin.display(description='Nombre', ordering='name')
    def name_display(self, obj):
        return format_html(f'<b>{obj.name}</b>')
    
    @admin.display(description='Valor', ordering='value')
    def value_display(self, obj):
        return format_html(f'<code style="background-color: #f8f9fa; padding: 2px 6px; border-radius: 3px;">{obj.value}</code>')
    
    @admin.display(description='Tipo')
    def type_badge(self, obj):
        return format_html('<span style="background-color: #FFF9C4; padding: 3px 10px; border-radius: 3px;">Variable</span>')