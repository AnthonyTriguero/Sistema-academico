from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.utils import timezone
import socket



def movimientos(request):

    if 'usuario' in request.session:
        return render(request,'sistemaAcademico/Admision/movimientos.html')
    else:
        return HttpResponseRedirect('timeout/')