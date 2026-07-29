from django.shortcuts import render

# Create your views here.

def compiler_view(request):
    return render(request, "compiler.html")