from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.utils import timezone
import socket


def consultas(request):

    if 'usuario' in request.session:
        return render(request,'sistemaAcademico/Admision/consultas.html')
    else:
        return HttpResponseRedirect('../')