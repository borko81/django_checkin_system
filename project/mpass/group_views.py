from django.shortcuts import render, redirect, get_object_or_404
from .models import GroupModel
from django.http import JsonResponse
import json


def groups(request):
    obj = GroupModel.objects.all()
    context = {
        "obj": obj,
        'title': 'All Groups'
    }
    return render(request, 'mpass/groups.html', context=context)


def new_group(request):
    if request.method == 'POST':
        name = json.loads(request.body)
        # import pdb;pdb.set_trace()
        try:
            g = GroupModel.objects.create(name=name['name'])
            g.save()
            return redirect('groups')
        except:
            return redirect('groups')
    else:
        return redirect('groups')


def group_edit(request, id_, new_name=None):
    obj = get_object_or_404(GroupModel, id=id_)
    try:
        obj.name = new_name
        obj.save()
    except:
        return JsonResponse("error", safe=False)
    else:
        return JsonResponse("Ok", safe=False)


def group_delete(request, id_):
    obj = get_object_or_404(GroupModel, id=id_)
    try:
        obj.delete()
    except:
        return JsonResponse("Error when try to delete")
    else:
        return redirect('groups')
