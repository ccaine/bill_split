from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('splitter/', include('splitter.urls')),
    path('admin/', admin.site.urls),
]