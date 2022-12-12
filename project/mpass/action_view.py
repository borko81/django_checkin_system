from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from decouple import config

from .models import ActionModel, CardsModel, ActionModel, OnlyInHouse

from datetime import date


def show_in_out(request):
	card_number = None
	action = ActionModel.objects.all().order_by('-data_time')[:int(config('SHOW_COUNT'))]
	context = {
		"title": "Action",
		"actions": action,
		"message": None
	}
	today = date.today()

	if request.method == 'POST':
		card_number = request.POST.get('card')
		try:
			card = CardsModel.objects.get(card=card_number)
		except:
			context['message'] = "Card not recognize"
			return render(request, template_name='mpass/magic.html', context=context)

		if card.person_id is not None:
			if card.valid_from is not None and card.valid_to is not None:
				if card.valid_from > today or card.valid_to < today:
					context['message'] = "Card period is expired"
					return render(request, template_name='mpass/magic.html', context=context)

			reverse_action = 'IN'
			last_action = 'OUT'
			try:
				last_action = ActionModel.objects.filter(card_id__card=card_number).last().action
			except:
				pass
			if last_action == 'IN':
				reverse_action = 'OUT'
				
			new_action = ActionModel(card_id=card, person_id=card.person_id, action=reverse_action)
			new_action.save()

			context['message'] = f"{reverse_action}"

		else:
			context['message'] = "Card not recognize"

	return render(request, template_name='mpass/magic.html', context=context)