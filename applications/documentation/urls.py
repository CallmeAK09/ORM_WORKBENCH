from django.contrib import admin
from django.urls import path
from applications.documentation.views import documentation_view

urlpatterns = [
    path("", documentation_view, name=("documentation")),
]
