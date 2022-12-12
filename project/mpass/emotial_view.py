from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import OnlyInHouse


@login_required
def show_all_in_house(request):
    context = {"people_in_house": OnlyInHouse.objects.all()}
    return render(request, template_name="mpass/in_house.html", context=context)
