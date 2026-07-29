from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("applications.compiler.urls")),
    path("document/", include("applications.documentation.urls")),
]