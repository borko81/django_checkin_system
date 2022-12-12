from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import CardsModel
from .forms import forms


card_query_mapper = {
    "without_person": CardsModel.custom_manager.without_person(),
    "stoped": CardsModel.custom_manager.stoped_card(),
}


@login_required
def show_all_cards(request):
    """Show cards"""

    order_by = request.GET.get("order")

    cards = card_query_mapper.get(order_by, CardsModel.objects.all())

    context = {"all_cards": cards, "title": "All Cards"}

    return render(request, template_name="mpass/all_cards.html", context=context)


@login_required
def create_new_card(request):
    form = forms.CardForm(request.POST or None)
    context = {"form": form, "title": "New/Edit Card"}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("show_all_cards")
    return render(request, template_name="mpass/new_cards.html", context=context)


@login_required
def edit_card(request, id_):
    obj = get_object_or_404(CardsModel, id=id_)
    form = forms.CardForm(request.POST or None, instance=obj)
    context = {"title": "Edit Card", "form": form}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("show_all_cards")
    return render(request, template_name="mpass/new_cards.html", context=context)


@login_required
def show_custom_card(request, id_):
    """Return custom cards by id, maybe from something else"""
    pass


@login_required
def delete_card(request, id_):
    card = get_object_or_404(CardsModel, id=id_)
    card.delete()
    return redirect("show_all_cards")
