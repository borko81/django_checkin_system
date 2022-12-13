from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import OnlyInHouse, ActionModel

import datetime


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


@login_required
def total_time_in_house(request):
    context = {
        "title": "Total Time"
    }


    if request.method == 'POST':
        passage_from = request.POST.get('from')
        passage_to = request.POST.get('to')

        if passage_from != '' and passage_to != '':
            result = ActionModel.objects.filter(data_time__gte=passage_from, data_time__lte=passage_to).order_by("id")

            persons = set(i.person_id.name for i in result)
            person_time = {}
            for name in persons:

                name_time = 0

                if name not in person_time:
                    person_time[name] = 0

                temporary_data = [(i.action, i.data_time) for i in result if i.person_id.name == name]

                for line in range(len(temporary_data)):
                    if line == 0 and temporary_data[line][0] == "OUT":
                        continue

                    if temporary_data[line][0] == "OUT":
                        name_time += (temporary_data[line][1] - temporary_data[line - 1][1]).total_seconds()

                person_time[name] = str(datetime.timedelta(seconds=name_time))

            context["details"] = dict(sorted(person_time.items(), key=lambda x: x[0]))


    return render(request, template_name="mpass/total_time_in_house.html", context=context)
