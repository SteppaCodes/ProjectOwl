
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("manager.urls")),
    path("", include("project_manager.urls")),
]

