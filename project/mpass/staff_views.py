from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import PersonInformationModel
from .forms import forms
from .helpers.debuger import debug


@login_required
def persons(request):
    """Return all persons (staff) information via list"""

    order_by = request.GET.get("order_by")
    persons = PersonInformationModel.objects.all()

    if order_by:
        persons = PersonInformationModel.objects.filter(group__name=order_by)

    list_count_in_groups = [p.group.name for p in PersonInformationModel.objects.all()]
    count_person_in_groups = {
        name: list_count_in_groups.count(name) for name in list_count_in_groups
    }

    context = {
        "persons": persons,
        "count_person_in_groups": count_person_in_groups,
        "title": "Staff",
    }
    return render(request, "mpass/staff.html", context=context)


@login_required
def new_person(request, id_=None):
    """Create new or edit person"""
    form = forms.PersonForm(request.POST or None, request.FILES or None)

    if id_:
        obj = get_object_or_404(PersonInformationModel, id=id_)
        form = forms.PersonForm(
            request.POST or None, request.FILES or None, instance=obj
        )

    context = {"form": form}

    if request.method == "GET":
        return render(request, "mpass/new_staff.html", context=context)

    elif request.method == "POST":

        if form.is_valid():
            form.save()
            return redirect("persons")
        context["messages"] = "Errors occuired"
        return render(request, "mpass/new_staff.html", context=context)


@login_required
def delete_person(request, id_):
    obj = get_object_or_404(PersonInformationModel, id=id_)
    obj.delete()
    return redirect("persons")


@login_required
def person_detail(request, id_):
    obj = get_object_or_404(PersonInformationModel, id=id_)
    d = obj.to_dict()
    d["picture"] = str(d["picture"])
    return JsonResponse(d)
