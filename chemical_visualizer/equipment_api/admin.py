"""
Admin configuration for equipment_api.
"""
from django.contrib import admin
from equipment_api.models import EquipmentUpload


@admin.register(EquipmentUpload)
class EquipmentUploadAdmin(admin.ModelAdmin):
    """Admin interface for EquipmentUpload model."""
    list_display = ('filename', 'uploaded_at', 'equipment_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature')
    list_filter = ('uploaded_at',)
    search_fields = ('filename',)
    readonly_fields = ('filename', 'uploaded_at', 'equipment_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature', 'type_distribution')
