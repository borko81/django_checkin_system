from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import GroupModel
from django.http import JsonResponse
import json


@login_required
def index(request):
    context = {"title": "index"}
    return render(request, "mpass/base.html", context=context)
