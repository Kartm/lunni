from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
