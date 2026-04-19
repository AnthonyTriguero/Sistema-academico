from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.utils import timezone
import socket


def procesos(request):

    if 'usuario' in request.session:
        return render(request,'sistemaAcademico/Admision/procesos.html')
    else:
        return HttpResponseRedirect('../')
