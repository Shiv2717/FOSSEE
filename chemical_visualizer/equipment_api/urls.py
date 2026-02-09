"""
URL configuration for equipment_api app.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from equipment_api.views import EquipmentUploadViewSet

router = DefaultRouter()
router.register(r'', EquipmentUploadViewSet, basename='equipment')

urlpatterns = router.urls

# Alternative explicit URL patterns:
# urlpatterns = [
#     path('upload/', EquipmentUploadViewSet.as_view({'post': 'upload'}), name='equipment-upload'),
#     path('history/', EquipmentUploadViewSet.as_view({'get': 'history'}), name='equipment-history'),
# ]
