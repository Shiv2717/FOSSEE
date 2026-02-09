"""
Models for equipment API - stores CSV upload history and statistics.
"""
from django.db import models
from django.utils import timezone


class EquipmentUpload(models.Model):
    """
    Stores summary of equipment CSV uploads.
    Only keeps last 5 uploads (managed via manager).
    """
    # Upload metadata
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Statistics
    equipment_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    
    # Equipment type distribution (stored as JSON string)
    type_distribution = models.TextField()  # JSON format: {"type1": count, "type2": count}
    
    class Meta:
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    @staticmethod
    def cleanup_old_uploads():
        """Keep only the last 5 uploads."""
        old_ids = list(
            EquipmentUpload.objects.order_by('-uploaded_at')
            .values_list('id', flat=True)[5:]
        )
        if old_ids:
            EquipmentUpload.objects.filter(id__in=old_ids).delete()
