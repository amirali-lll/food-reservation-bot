from django.shortcuts import render

def api_home(request):
    return render(request, 'index.html')