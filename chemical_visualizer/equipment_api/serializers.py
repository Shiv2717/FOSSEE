"""
Serializers for equipment API - converts models to JSON and validates data.
"""
from rest_framework import serializers
from equipment_api.models import EquipmentUpload
import json


class EquipmentUploadSerializer(serializers.ModelSerializer):
    """Serializer for equipment upload history."""
    
    # Parse type_distribution from JSON string to dict
    type_distribution = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentUpload
        fields = [
            'id',
            'filename',
            'uploaded_at',
            'equipment_count',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'type_distribution',
        ]
        read_only_fields = [
            'id',
            'filename',
            'uploaded_at',
            'equipment_count',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'type_distribution',
        ]
    
    def get_type_distribution(self, obj):
        """Convert JSON string to dict."""
        try:
            return json.loads(obj.type_distribution)
        except (json.JSONDecodeError, TypeError):
            return {}


class CSVUploadSerializer(serializers.Serializer):
    """Serializer for CSV file upload."""
    csv_file = serializers.FileField(
        required=True,
        help_text="CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature"
    )
    
    def validate_csv_file(self, value):
        """Validate that the uploaded file is a CSV."""
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File must be a CSV file.")
        return value
