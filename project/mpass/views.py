from django.shortcuts import render, redirect, get_object_or_404
from .models import GroupModel
from django.http import JsonResponse
import json


def index(request):
    context = {}
    return render(request, 'mpass/base.html', context=context)



