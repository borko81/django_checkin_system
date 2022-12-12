from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import GroupModel

import json


@login_required
def groups(request):
    obj = GroupModel.objects.all()
    context = {
        "obj": obj,
        'title': 'All Groups'
    }
    return render(request, 'mpass/groups.html', context=context)


@login_required
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


@login_required
def group_edit(request, id_, new_name=None):
    obj = get_object_or_404(GroupModel, id=id_)
    try:
        obj.name = new_name
        obj.save()
    except:
        return JsonResponse("error", safe=False)
    else:
        return JsonResponse("Ok", safe=False)


@login_required
def group_delete(request, id_):
    obj = get_object_or_404(GroupModel, id=id_)
    try:
        obj.delete()
    except:
        return JsonResponse("Error when try to delete")
    else:
        return redirect('groups')
