from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import OnlyInHouse, ActionModel


@login_required
def show_all_in_house(request):
    context = {"people_in_house": OnlyInHouse.objects.all(), "title": "InOut"}
    return render(request, template_name="mpass/in_house.html", context=context)


@login_required
def passage(request):
    context = {
        "title": "Passage"
    }

    if request.method == 'POST':
        passage_from = request.POST.get('from')
        passage_to = request.POST.get('to')

        if passage_from != '' and passage_to != '':
            result = ActionModel.objects.filter(data_time__gte=passage_from, data_time__lte=passage_to).order_by("person_id__name")
            context["result"] = result
            context["persons"] = set(i.person_id.name for i in result)

    return render(request, template_name="mpass/passage.html", context=context)