from django.shortcuts import render, redirect
from django.views import View

from applications.compiler.services.compiler_service import (
    reset_session_service, execute_query_service, save_model_service, build_context_service
    )


def compiler_view(request):
    context = build_context_service(request)
    return render(request, "compiler.html", context) 


def reset_session(request):
    reset_session_service(request)
    return redirect('compiler')


def execute_query(request):
    return execute_query_service(request)


def save_model(request):
    return save_model_service(request)