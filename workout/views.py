# coding=utf-8
# decoding=utf-8
# Python imports
# Django imports
from django.shortcuts import render, redirect
# Third party app imports
# Local app imports
from .models import BodyPart, Exercise, ExerciseSet, Routine


# Create your views here.
def bodypart_view(request):

    # Se genera el contexto con toda la información y se renderiza
    context = {
    }
    return render(request, 'index.html', context)


def exercise_view(request):

    # Se genera el contexto con toda la información y se renderiza
    context = {
    }
    return render(request, 'index.html', context)


def routine_view(request):

    # Se genera el contexto con toda la información y se renderiza
    context = {
    }
    return render(request, 'index.html', context)