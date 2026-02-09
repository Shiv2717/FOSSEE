"""
URL configuration for chemical_visualizer project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    """API root endpoint"""
    return JsonResponse({
        'message': 'Chemical Equipment Visualizer API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'upload': '/api/upload/',
            'history': '/api/history/',
            'report': '/api/report/',
        },
        'auth': 'HTTP Basic Authentication',
        'credentials': 'username: admin, password: admin123'
    })

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/', include('equipment_api.urls')),
]
