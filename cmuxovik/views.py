from django.shortcuts import render
from .models import Cmux


def home(request):
    cmuxes = Cmux.objects.all()[:5]
    
    return render(request, 'cmuxovik/home.html', {'cmuxes': cmuxes})
