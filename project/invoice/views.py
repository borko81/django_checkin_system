from django.shortcuts import render, redirect

from .models import Contragent, OwnerNumbers, FakElelements, FakId, OwnerModel, BankAcc, Contragent

from decimal import Decimal


def show_invoice(request, id_):
	owner = OwnerModel.objects.first()
	bank = BankAcc.objects.get(owner_id=owner.id)
	fak_id = FakId.objects.get(id=id_)
	fak_elementrs = FakElelements.objects.filter(faktura_id=fak_id.id)
	contract_id = Contragent.objects.get(id=fak_id.contract_id.id)
	context = {
		"title": "Show invoice",
		"id": fak_id,
		'bases': fak_id.fak_total - fak_id.dds_suma,
		"owner": owner,
		"bank": bank,
		"contract": contract_id,
		'elements': fak_elementrs
	}
	return render(request, template_name='invoice/show_template.html', context=context)


def generate_fac(request):
	context = {
		"title": "Show invoice",
		"contracts": Contragent.objects.filter(is_active=True)
	}
	if request.method == "POST":
		request_data = {
			"fak_type": request.POST.get('fak_type'),
			"fak_pay": request.POST.get('fak_pay'),
			"contragent_id": Contragent.objects.get(id=request.POST.get('contragent_id')),
			"name": request.POST.get('name'),
			"q": int(request.POST.get('q')),
			"brut": Decimal(request.POST.get('brut')),
			"dds": int(request.POST.get('dds')),
		}

		f_eleements = FakElelements(
			text=request_data['name'],
			kol=request_data['q'],
			brutna_cena=request_data['brut'],
			dds=int(request_data['dds'])
		)
		f_eleements.save()
		fak_id = FakId.objects.filter(number=f_eleements.faktura_id.number)[0]
		fak_id.contract_id = request_data['contragent_id']

		fak_id.save()

		return redirect('show_invoice', id_=fak_id.id)

	return render(request, template_name='invoice/generate_fac.html', context=context)