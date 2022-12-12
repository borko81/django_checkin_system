from django.shortcuts import render
from .models import OnlyInHouse


def show_all_in_house(request):
	context = {
		"people_in_house": OnlyInHouse.objects.all()
	}
	return render(request, template_name='mpass/in_house.html', context=context)