from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("", views.compiler_view, name="compiler"),
    path("reset/", views.reset_session, name="reset"),
    path("api/save_models/", views.save_model, name="save_models"),
    path("api/execute/", views.execute_query, name="execute_query"),
]

