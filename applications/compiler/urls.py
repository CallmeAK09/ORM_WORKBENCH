from django.contrib import admin
from django.urls import path
from applications.compiler.views import compiler_view

urlpatterns = [
    path("", compiler_view, name=("compiler")),
]
