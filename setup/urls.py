from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('cubo_data.urls')),
    path('conferencias/', include('conferencias.urls', namespace='conferencias')),
    
]
